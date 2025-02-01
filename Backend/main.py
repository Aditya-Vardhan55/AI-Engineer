from fastapi import FastAPI
from routes.file_routes import router as file_router

app = FastAPI(title="AI-Powered Engineer API")

# Include file handling routes
app.include_router(file_router, prefix="/files")

@app.get("/")
async def root():
    return {"message":"Welcome to AI-Powered Engineer!"}
