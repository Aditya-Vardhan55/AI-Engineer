from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import SessionLocal
from services.retrieval_service import store_query_embedding, retrieve_similar_queries

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@router.post("/store/")
async def store_query(query: str, response: str, db: Session = Depends(get_db)):
    interaction_id = store_query_embedding(db, query, response)
    return {"message": "Stored successfully!", "interaction_id": interaction_id}

@router.get("/retrieve/")
async def retrieve_queries(query: str):
    results = retrieve_similar_queries(query)
    return {"similar_queries": results}