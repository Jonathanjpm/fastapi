from main import app
from fastapi import status
from fastapi.testclient import TestClient
from core.constants import *


client = TestClient(app)

def test_article_not_found():
    response = client.get("/articles/3a4e88bc-68cf-4abc-82e9-c26a6f245fb6")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == NOT_FOUND

def test_create_and_get():
    payload = {
        "title": "Teclado Mecanico",
        "body": "Red Switch",
        "tags": "ergonomico,TKL,70%",
        "author": "Jonathan Perez Medina",
        "published_at": "2025-10-05 00:00:00"
    }
    response = client.post("/articles", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(f"/articles/{response.json()["id"]}")
    assert response.status_code == status.HTTP_200_OK

    response = client.delete(f"/articles/{response.json()["id"]}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_create_and_update():
    payload = {
        "title": "Teclado Mecanico",
        "body": "Blue Switch",
        "tags": "Ergonomico,TKL,100%",
        "author": "Rocket Code",
        "published_at": "2025-10-05 00:00:00"
    }
    response = client.post("/articles", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    payload = {
        "body": "Blue Switch",
        "tags": "Ergonomico,TKL,100%,Hot Swap",
        "published_at": "2025-10-05 01:01:01"
    }
    response = client.put(f"/articles/{response.json()["id"]}", json=payload)
    assert response.status_code == status.HTTP_200_OK

    response = client.delete(f"/articles/{response.json()["id"]}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_create_and_search():
    payload = {
        "title": "Teclado Mecanico",
        "body": "Blue Switch",
        "tags": "Ergonomico,TKL,100%",
        "author": "Rocket Code",
        "published_at": "2025-10-05 00:00:00"
    }
    response = client.post("/articles", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    search="page=1&size=2&author=Code&tags=TKL"
    response_search = client.get(f"/articles?{search}")
    assert response_search.status_code == status.HTTP_200_OK

    response = client.delete(f"/articles/{response.json()["id"]}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_validate_unique_constrain():
    payload = {
        "title": "Teclado Mecanico",
        "body": "Blue Switch",
        "tags": "Ergonomico,TKL,100%",
        "author": "Rocket Code",
        "published_at": "2025-10-05 00:00:00"
    }

    id = None
    for number in range(0,2):
        response = client.post("/articles", json=payload)
        if response.status_code == status.HTTP_201_CREATED:
            id = response.json()["id"]
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            assert response.json()["detail"] == DUPLICATE_ARTICLES

    response = client.delete(f"/articles/{id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_validate_cache():
    payload = {
        "title": "Teclado Mecanico",
        "body": "Red Switch",
        "tags": "ergonomico,TKL,70%",
        "author": "Jonathan Perez Medina",
        "published_at": "2025-10-05 00:00:00"
    }
    response = client.post("/articles", json=payload)
    assert response.status_code == status.HTTP_201_CREATED

    response = client.get(f"/articles/{response.json()["id"]}")
    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/articles/{response.json()["id"]}")
    assert response.status_code == status.HTTP_200_OK

    response = client.get(f"/articles/{response.json()["id"]}")
    assert response.status_code == status.HTTP_200_OK

    response = client.delete(f"/articles/{response.json()["id"]}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

