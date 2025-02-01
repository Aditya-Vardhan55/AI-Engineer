from .database import Base
from sqlalchemy import Column, Integer, Text

class Interaction(Base):
    __tablename__ = "interactions"
    
    id = Column(Integer, primary_key= True, index= True)
    user_query = Column(Text, nullable= False)
    ai_response = Column(Text, nullable= False)
    feedback = Column(Integer, default= 0)  # 1=good, -1=bad