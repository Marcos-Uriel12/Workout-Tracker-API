from app.database import SessionLocal
from app.models.models import Exercise

exercises = [
    {"name": "Press de banca", "description": "Ejercicio de pecho con barra", "category": "strength"},
    {"name": "Sentadilla", "description": "Ejercicio de piernas con barra", "category": "strength"},
    {"name": "Peso muerto", "description": "Ejercicio de espalda y piernas", "category": "strength"},
    {"name": "Dominadas", "description": "Ejercicio de espalda con peso corporal", "category": "strength"},
    {"name": "Curl de bicep", "description": "Ejercicio de bicep con mancuernas", "category": "strength"},
    {"name": "Correr", "description": "Cardio en cinta o exterior", "category": "cardio"},
    {"name": "Bicicleta", "description": "Cardio en bicicleta estática o exterior", "category": "cardio"},
    {"name": "Saltar soga", "description": "Cardio con soga", "category": "cardio"},
    {"name": "Yoga", "description": "Ejercicios de flexibilidad y respiración", "category": "flexibility"},
    {"name": "Stretching", "description": "Estiramientos generales", "category": "flexibility"},
]

def seed():
    db = SessionLocal()
    try:
        existing = db.query(Exercise).first()
        if existing:
            print("DB already seeded")
            return
        
        for ex in exercises:
            db.add(Exercise(**ex))
        db.commit()
        print(f"{len(exercises)} exercises seeded")
    finally:
        db.close()

if __name__ == "__main__":
    seed()