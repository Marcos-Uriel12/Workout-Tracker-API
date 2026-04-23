from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.models import Workout, WorkoutExercise, Exercise
from app.utils import get_current_user
from app.models.models import User
from app.schemas.workouts import WorkoutCreate, WorkoutResponse, WorkoutExerciseCreate, WorkoutExerciseResponse,WorkoutUpdate
from datetime import datetime


router = APIRouter(prefix="/workouts", tags=["workouts"])

@router.put("/{workout_id}", response_model=WorkoutResponse)
def update_workout(workout_id: int, workout_data: WorkoutUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == current_user.id).first()
    print(f"Buscando workout_id={workout_id}, user_id={current_user.id}")
    result = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == current_user.id).first()
    print(f"Resultado: {result}")

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    if workout_data.name is not None:
        workout.name = workout_data.name
    if workout_data.notes is not None:
        workout.notes = workout_data.notes
    if workout_data.date is not None:
        workout.date = workout_data.date


    if workout_data.exercises is not None:
        db.query(WorkoutExercise).filter(WorkoutExercise.workout_id == workout_id).delete()
        for ex in workout_data.exercises:
            exercise = db.query(Exercise).filter(Exercise.id == ex.exercise_id).first()
            if not exercise:
                raise HTTPException(status_code=404, detail=f"Exercise {ex.exercise_id} not found")
            db.add(WorkoutExercise(
                workout_id=workout.id,
                exercise_id=ex.exercise_id,
                num_sets=ex.num_sets,
                num_reps=ex.num_reps,
                weight=ex.weight
            ))
            
    db.commit()
    db.refresh(workout)
    return workout


@router.post("/", response_model=WorkoutResponse, status_code=201)
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_workout = Workout(
        name=workout.name,
        notes=workout.notes,
        date=workout.date or datetime.utcnow(),
        user_id=current_user.id
    )
    db.add(new_workout)
    db.flush()

    for ex in workout.exercises:
        exercise = db.query(Exercise).filter(Exercise.id == ex.exercise_id).first()
        if not exercise:
            raise HTTPException(status_code=404, detail=f"Exercise {ex.exercise_id} not found")
        db.add(WorkoutExercise(
            workout_id=new_workout.id,
            exercise_id=ex.exercise_id,
            num_sets=ex.num_sets,
            num_reps=ex.num_reps,
            weight=ex.weight
        ))

    db.commit()
    db.refresh(new_workout)
    return new_workout

@router.get("/", response_model=list[WorkoutResponse])
def get_workouts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Workout).filter(Workout.user_id == current_user.id).all()

@router.get("/{workout_id}", response_model=WorkoutResponse)
def get_workout(workout_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == current_user.id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@router.delete("/{workout_id}", status_code=204)
def delete_workout(workout_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == current_user.id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(workout)
    db.commit()


@router.get("/progress/{exercise_id}")
def get_exercise_progress(exercise_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    history = db.query(WorkoutExercise)\
        .join(Workout)\
        .filter(WorkoutExercise.exercise_id == exercise_id)\
        .filter(Workout.user_id == current_user.id)\
        .order_by(Workout.date.asc())\
        .all()

    return {
        "exercise": exercise.name,
        "history": [
            {
                "date": item.workout.date,
                "num_sets": item.num_sets,
                "num_reps": item.num_reps,
                "weight": item.weight
            }
            for item in history
        ]
    }    

