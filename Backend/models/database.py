from sqlalchemy import create_engine, Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./learning.db"    # Change to PostgreSQL if needed to change

engine = create_engine(DATABASE_URL, connect_args={"check_sam_thread": False}) 
SessionLocal = sessionmaker(bind= engine, autocommit= False, autoflush= False)
Base = declarative_base()