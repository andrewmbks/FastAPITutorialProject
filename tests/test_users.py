from app import schemas
from .database import client, session   

def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to my API'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "testuser1@gmail.com", "password": "1234"})
    print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "testuser1@gmail.com"
    assert res.status_code == 201