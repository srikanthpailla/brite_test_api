import unittest
import sys
import os
from unittest import mock
from fastapi.testclient import TestClient
from database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

mock_operations = mock.MagicMock()
sys.modules["operations"] = mock_operations
from main import get_db, app, models

SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

mock_data = {
    "id": 1,
    "imdbid": "tt0096895",
    "title": "Batman",
    "year": 1989,
    "genre": "Action, Adventure",
    "released": "23 Jun 1989",
    "language": "English, French, Spanish",
    "director": "Tim Burton",
    "writer": "Bob Kane, Sam Hamm, Warren Skaaren",
    "actors": "Michael Keaton, Jack Nicholson, Kim Basinger",
}


def test_root_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "FastAPI - Swagger UI" in response.text


def test_single_route_failure():
    response = client.get("/single?title=Batman")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}


def test_add():
    mock_operations.Operations().add_movie.return_value = models.Movie(**mock_data)
    response = client.post("/add?title=Batman")
    assert response.status_code == 200
    assert response.json() == mock_data


def test_list_route():
    response = client.get("/list?page=1&perpage=10")
    assert response.status_code == 200
    assert response.json() == {
        "items": [mock_data],
        "page": 1,
        "pages": 1,
        "size": 10,
        "total": 1,
    }


def test_single_route_without_title():
    response = client.get("/single")
    assert response.status_code == 200
    assert response.json() == mock_data


def test_single_route_with_title():
    response = client.get("/single?title=Batman")
    assert response.status_code == 200
    assert response.json() == mock_data


def test_delete_route():
    response = client.delete("/remove?id=1")
    assert response.status_code == 200
    assert response.json() == {"1 row": "removed"}


def test_delete_route_failure():
    response = client.delete("/remove?id=123")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie with id: 123 not found"}
