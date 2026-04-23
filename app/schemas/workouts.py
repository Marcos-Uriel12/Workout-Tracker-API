from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class ExerciseInWorkout(BaseModel):
    id: int
    name: str
    category: Optional[str] = None

    class Config:
        from_attributes = True

class WorkoutExerciseCreate(BaseModel):
    exercise_id: int
    num_sets: int
    num_reps: int
    weight: Optional[float] = None

class WorkoutExerciseResponse(BaseModel):
    id: int
    exercise: ExerciseInWorkout
    num_sets: int
    num_reps: int
    weight: Optional[float] = None

    class Config:
        from_attributes = True

class WorkoutCreate(BaseModel):
    name: str
    notes: Optional[str] = None
    date: Optional[datetime] = None
    exercises: Optional[list[WorkoutExerciseCreate]] = []

class WorkoutResponse(BaseModel):
    id: int
    name: str
    notes: Optional[str] = None
    date: datetime
    created_at: datetime
    exercises: list[WorkoutExerciseResponse] = []

    class Config:
        from_attributes = True
        
class WorkoutUpdate(BaseModel):
    name: Optional[str] = None
    notes: Optional[str] = None
    date: Optional[datetime] = None
    exercises: Optional[list[WorkoutExerciseCreate]] = None