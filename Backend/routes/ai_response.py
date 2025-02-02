from fastapi import APIRouter
from services.ai_response_service import generate_ai_response

router = APIRouter()

@router.post("/generate-response/")
async def get_ai_response(query: str):
    response = generate_ai_response(query)
    return {"query": query, "ai_response": response}