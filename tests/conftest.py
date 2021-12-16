import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    # print("\nRunning Session Fixture...\nSession Up...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    # print("\nClosing Session")

@pytest.fixture
def client(session):
    # print("Running Client Fixture..")
    def override_get_db():
        try:
           yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    # print("Client Fixture Complete")
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    # print("Creating Test User...")
    user_data = {"email": "testuser0@gmail.com", "password": "1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    # print("Test User Successfully Created")
    return new_user


@pytest.fixture
def test_user2(client):
    # print("Creating Test User...")
    user_data = {"email": "testuser00@gmail.com", "password": "1234"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    # print("Test User Successfully Created")
    return new_user


@pytest.fixture
def token(test_user):
    # print("Generating JWT...")
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    # print("Authorizing Client...")
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    # print("Client Successfully Authorized")
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    # print("Creating Test Posts...")
    posts_data = [{
        "title": "1st title",
        "content": "1st content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']
    }]
    
    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)

    session.commit()

    posts = session.query(models.Post).all()
    # print("Test Posts Successfully Created")
    return posts