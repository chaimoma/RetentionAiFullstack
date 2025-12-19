from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db, User, PredictionHistory
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from pydantic import BaseModel
import joblib
import os
from pathlib import Path
from google import genai
import pandas as pd
import json  
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="RetentionAI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DbDep = Depends(get_db)
client = genai.Client(api_key=os.getenv("GEMINI_KEY"))

# ---------------- pydantic models ----------------

class UserBase(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class EmployeeData(BaseModel):
    employee_id: str 
    Age: int
    BusinessTravel: str
    Department: str
    Education: int
    EducationField: str
    EnvironmentSatisfaction: int
    Gender: str
    JobInvolvement: int
    JobLevel: int
    JobRole: str
    JobSatisfaction: int
    MaritalStatus: str
    MonthlyIncome: float
    OverTime: str
    PerformanceRating: int
    RelationshipSatisfaction: int
    StockOptionLevel: int
    TotalWorkingYears: int
    WorkLifeBalance: int
    YearsAtCompany: int
    YearsInCurrentRole: int
    YearsWithCurrManager: int

class RetentionRequest(EmployeeData):
    churn_probability: float

# ---------------- endpoints ----------------

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

# load ml model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml" / "notebook" / "LogisticRegression_model.pkl"
model = joblib.load(MODEL_PATH)

@app.post("/predict")
def predict(employee: EmployeeData, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    data = employee.model_dump()
    employee_id = data.pop("employee_id")
    X = pd.DataFrame([data])

    probability = model.predict_proba(X)[0][1]

    history = PredictionHistory(
        user_id=current_user.id,
        employee_id=employee_id,
        probability=float(probability)
    )
    db.add(history)
    db.commit()

    return {"churn_probability": round(probability, 2)}

@app.post("/generate-retention-plan")
def generate_retention_plan(request: RetentionRequest, current_user: User = Depends(get_current_user)):
    if request.churn_probability <= 0.5:
        return {"retention_plan": ["Churn risk is low. No retention action needed."]}

    prompt = f"""
Agis comme un expert RH.

Voici les informations sur l’employé :
- Age : {request.Age}
- Département : {request.Department}
- Rôle : {request.JobRole}
- Satisfaction : {request.JobSatisfaction}
- Performance : {request.PerformanceRating}
- Équilibre vie pro/perso : {request.WorkLifeBalance}
- Heures supplémentaires : {request.OverTime}

Contexte : ce salarié a un risque élevé de départ ({request.churn_probability*100:.0f}%).

Tâche :
Propose exactement 3 actions RH concrètes pour améliorer sa rétention.
Les actions doivent être courtes (une seule ligne chacune, sans explication).

Réponds uniquement au format JSON suivant :
{{
  "retention_plan": ["action 1", "action 2", "action 3"]
}}
"""
    
    try:
        gem_resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        raw_text = gem_resp.text.strip()   
        if raw_text.startswith("```"):
            raw_text = "\n".join(raw_text.split("\n")[1:-1])
        gem_data = json.loads(raw_text)
    except Exception:
        gem_data = {
            "retention_plan": [
                "Proposer 2 jours de télétravail",
                "Réévaluer la charge de déplacement",
                "Plan de formation personnalisé"
            ]
        }

    return {"retention_plan": gem_data["retention_plan"]}

@app.get("/prediction-history")
def get_prediction_history(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user) 
):
    history = db.query(PredictionHistory).filter(PredictionHistory.user_id == current_user.id).all()
    return history