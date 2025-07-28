from fastapi import FastAPI
from app.api.init import api_router
from app.db.database import engine, Base


app = FastAPI()

# Create all tables from models
Base.metadata.create_all(bind=engine)
app.include_router(api_router, prefix="/api")
