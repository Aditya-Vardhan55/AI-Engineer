from fastapi import FastAPI
from routes.file_routes import router as file_router
from routes.execute import router as execute_router

app = FastAPI(title="AI-Powered Engineer API")

# Include routes
app.include_router(file_router, prefix="/files")
app.include_router(execute_router, prefix="/run")

@app.get("/")
async def root():
    return {"message":"Welcome to AI-Powered Engineer!"}
