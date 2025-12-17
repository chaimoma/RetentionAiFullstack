from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db, User ,PredictionHistory
from app.auth import get_password_hash, verify_password, create_access_token,get_current_user
from pydantic import BaseModel
import joblib
from pathlib import Path
load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RetentionAI Backend")

DbDep = Depends(get_db)

# pydantic models

class UserBase(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class EmployeeData(BaseModel):
    Age: int
    BusinessTravel: str
    Department: str
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    JobRole: str
    MaritalStatus: str
    MonthlyIncome: float
    NumCompaniesWorked: int
    OverTime: str
    TotalWorkingYears: int
    TrainingTimesLastYear: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsSinceLastPromotion: int

# endpoints
@app.post("/register")
async def register_user(user: UserBase, db: Session = DbDep):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed = get_password_hash(user.password)
    new_user = User(username=user.username, password_hash=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully", "id": new_user.id, "username": new_user.username}

@app.post("/login")
async def login(user: UserBase, db: Session = DbDep):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    token = create_access_token({"user_id": db_user.id, "username": db_user.username})
    return {"access_token": token, "token_type": "bearer"}
# load model    
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "notebook" / "LogisticRegression_model.pkl"

model = joblib.load(MODEL_PATH)

