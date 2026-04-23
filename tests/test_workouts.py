def test_register_user(client):
    response = client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test User"
    assert response.json()["email"] == "test@test.com"

def test_login_user(client):
    # First, register the user
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "testpassword"
    })
    # Then, login the user
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_create_workout(client):
    # First, register and login the user to get the token
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "testpassword"
    })
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "testpassword"
    })
    token = response.json()["access_token"]

    # Then, create a workout
    workout_response = client.post("/workouts/", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "Morning Run"
    })
    assert workout_response.status_code == 201
    assert workout_response.json()["name"] == "Morning Run"

def test_get_workouts(client):
    # First, register and login the user to get the token
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "testpassword"
    })
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "testpassword"
    })
    token = response.json()["access_token"]

    # Then, get the workouts
    response = client.get("/workouts/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_workout(client):
    # First, register and login the user to get the token
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "testpassword"
    })
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    
    workout_response = client.post("/workouts/", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "Morning Run"
    })
    workout_id = workout_response.json()["id"]

    # Then, update a workout
    response = client.put(f"/workouts/{workout_id}", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "Updated Workout",
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Workout"

def test_delete_workout(client):
    # First, register and login the user to get the token
    client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "testpassword"
    })
    response = client.post("/auth/login", data={
        "username": "test@test.com",
        "password": "testpassword"
    })
    token = response.json()["access_token"]
    
    response = client.post("/workouts/", headers={"Authorization": f"Bearer {token}"}, json={
        "name": "Morning Run"
    })
    workout_id = response.json()["id"]

    # Then, delete a workout
    response = client.delete(f"/workouts/{workout_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204