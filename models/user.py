from datetime import datetime
from db.base import Base
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey

class User(Base): #schema for user table
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True) # Microsoft ID
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    
