from fastapi import FastAPI
from app.routers import auth,workouts,exercises
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(auth.router)
app.include_router(workouts.router)
app.include_router(exercises.router)
