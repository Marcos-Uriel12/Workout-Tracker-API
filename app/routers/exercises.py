from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Workout, WorkoutExercise, Exercise
from app.utils import get_current_user
from app.models.models import User
from app.schemas.exercises import ExerciseCreate, ExerciseResponse

router = APIRouter(prefix="/exercises", tags=["exercises"])

@router.post("/", response_model=ExerciseResponse, status_code=201)
def create_exercise(exercise: ExerciseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_exercise = Exercise(
        name=exercise.name,
        description=exercise.description,
        category=exercise.category
    )
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise

@router.get("/", response_model=list[ExerciseResponse])
def get_exercises(db: Session = Depends(get_db)):
    return db.query(Exercise).all()

@router.delete("/{exercise_id}", status_code=204)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    db.delete(exercise)
    db.commit()