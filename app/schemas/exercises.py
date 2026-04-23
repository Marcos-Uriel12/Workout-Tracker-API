from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ExerciseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

class ExerciseResponse(ExerciseCreate):
    id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
