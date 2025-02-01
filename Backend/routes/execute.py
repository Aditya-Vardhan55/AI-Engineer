from fastapi import APIRouter, HTTPException
from services.execution_service import execute_python_code

router = APIRouter()

@router.post("/execute/")
async def execute_code(filename: str):
    try:
        output = execute_python_code(filename)
        return {"filename": filename, "output": output}
    except Exception as e:
        raise HTTPException(status_code= 500, detail=str(e))
