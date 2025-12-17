from sqlalchemy import create_engine,Column,Integer,String,DateTime,Float,ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()
# Tables
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    predictions = relationship("PredictionHistory", back_populates="user")

class PredictionHistory(Base):
    __tablename__ = "predictions_history"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    employee_id = Column(String, nullable=False)
    probability = Column(Float, nullable=False)

    user = relationship("User", back_populates="predictions")


# db dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
