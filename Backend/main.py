from fastapi import FastAPI
from routes.file_routes import router as file_router
from routes.execute import router as execute_router
from routes.learning import router as learning_router
from models.database import engine, Base

app = FastAPI(title="AI-Powered Engineer API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routes
app.include_router(file_router, prefix="/files")
app.include_router(execute_router, prefix="/run")
app.include_router(learning_router, prefix="/learn")

@app.get("/")
async def root():
    return {"message":"Welcome to AI-Powered Engineer!"}
