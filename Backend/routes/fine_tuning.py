from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import SessionLocal
from services.fine_tuning_service import fine_tune_model

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/fine-tune/")
async def fine_tune(db: Session = Depends(get_db)):
    result = fine_tune_model(db)
    return {"message": result}