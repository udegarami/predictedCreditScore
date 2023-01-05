from typing import Optional
from pydantic import BaseModel 

class User(BaseModel):
    id: int
    gender: str
    carOwner : Optional[str]

class Query(BaseModel):
    id: str 
    gender: str 
    
class Prediction(BaseModel):
    id: str 
    score: float