from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import SessionLocal
from services.learning_service import store_interaction, retrieve_past_responses, update_feedback

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/store/")
async def store_query_response(query: str, response: str, db: Session = Depends(get_db)):
    interaction_id = store_interaction(db, query, response)
    return {"message": "Stored successfully!", "interaction_id": interaction_id}

@router.get("/retrieve/")
async def get_past_responses(query: str, db: Session = Depends(get_db)):
    responses = retrieve_past_responses(db, query)
    return {"responses": responses}

@router.put("/feedback/")
async def update_response_feedback(interaction_id: int, feedback: int, db: Session = Depends(get_db)):
    message = update_feedback(db, interaction_id, feedback)
    return {"message": message}
