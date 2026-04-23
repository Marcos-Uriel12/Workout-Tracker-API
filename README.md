# Workout Tracker API

REST API para registrar y seguir rutinas de ejercicio. Construida con FastAPI, SQLAlchemy y MySQL.

## Instalación y ejecución local

```bash
# Clonar el repositorio e instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (ver sección abajo)
cp .env.example .env

# Correr migraciones
alembic upgrade head

# Iniciar el servidor
uvicorn app.main:app --reload --port 8003
```

La API estará disponible en `http://localhost:8003`.  
Documentación interactiva: `http://localhost:8003/docs`

## Docker

```bash
docker compose up --build
```

- API: `http://localhost:8003`
- MySQL: `localhost:3309`

## Variables de entorno

| Variable       | Descripción                          | Ejemplo                                                |
|----------------|--------------------------------------|--------------------------------------------------------|
| `DATABASE_URL` | Cadena de conexión a MySQL           | `mysql+pymysql://root:pass@localhost:3306/workout_tracker` |
| `SECRET_KEY`   | Clave secreta para firmar JWT tokens | `una-clave-secreta-muy-larga`                          |

## Seeder

Carga datos iniciales de ejercicios en la base de datos:

```bash
python -m app.seeder
```

## Tests

```bash
pytest
```

## Endpoints

### Auth

| Método | Ruta             | Descripción                  | Auth |
|--------|------------------|------------------------------|------|
| POST   | `/auth/register` | Registrar nuevo usuario      | No   |
| POST   | `/auth/login`    | Login y obtención de JWT     | No   |

### Exercises

| Método | Ruta                  | Descripción            | Auth |
|--------|-----------------------|------------------------|------|
| GET    | `/exercises/`         | Listar ejercicios      | No   |
| POST   | `/exercises/`         | Crear ejercicio        | Sí   |
| DELETE | `/exercises/{id}`     | Eliminar ejercicio     | Sí   |

### Workouts

| Método | Ruta                            | Descripción                            | Auth |
|--------|---------------------------------|----------------------------------------|------|
| GET    | `/workouts/`                    | Listar workouts del usuario            | Sí   |
| POST   | `/workouts/`                    | Crear workout                          | Sí   |
| GET    | `/workouts/{id}`                | Obtener workout por ID                 | Sí   |
| PUT    | `/workouts/{id}`                | Actualizar workout                     | Sí   |
| DELETE | `/workouts/{id}`                | Eliminar workout                       | Sí   |
| GET    | `/workouts/progress/{exercise_id}` | Progreso histórico de un ejercicio  | Sí   |

> Los endpoints marcados con **Sí** requieren el header `Authorization: Bearer <token>`.

### Roadmap.sh

Url: https://roadmap.sh/projects/fitness-workout-tracker