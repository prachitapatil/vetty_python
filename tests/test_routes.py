import pytest
from unittest.mock import patch
from flask import Flask
import jwt
from datetime import datetime, timedelta
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.routes import main_bp 
from app.auth import auth_bp  

SECRET = "keypatil"


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.secret_key = SECRET
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    with app.test_client() as client:
        yield client


def test_login_success(client):
    response = client.post("/login", json={
        "username": "patil",
        "password": "patil1995"
    })
    data = response.get_json()

    assert response.status_code == 200
    assert "token" in data

def test_login_failure(client):
    response = client.post("/login", json={
        "username": "wrong",
        "password": "creds"
    })
    data = response.get_json()

    assert response.status_code == 401
    assert data["message"] == "Invalid credentials"

def get_token(client):
    response = client.post("/login", json={
        "username": "patil",
        "password": "patil1995"
    })
    return response.get_json()["token"]

# ---- /coins ----
def test_get_coins_with_token(client):
    token = get_token(client)
    response = client.get("/coins?page_num=1&per_page=5", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_coins_without_token(client):
    response = client.get("/coins")
    assert response.status_code == 401

# ---- /categories ----
def test_get_categories_with_token(client):
    token = get_token(client)
    response = client.get("/categories", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_categories_without_token(client):
    response = client.get("/categories")
    assert response.status_code == 401

# ---- /filtered-coins ----
def test_filtered_coins_with_token(client):
    token = get_token(client)
    response = client.get("/filtered-coins?id=bitcoin&page_num=1&per_page=2", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_filtered_coins_without_token(client):
    response = client.get("/filtered-coins")
    assert response.status_code == 401
