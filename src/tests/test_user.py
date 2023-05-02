import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
from core.config import settings
import pytest
import json

from main import app
from beanie.odm.utils.init import init_beanie

from motor.motor_asyncio import AsyncIOMotorClient
from models.user_model import User
from core.security import create_access_token, create_refresh_token


client = TestClient(app)

@pytest.fixture
async def test_db():
    test_db = settings.MONGO_CONNECTION_STRING.replace("weather", "weather_test")
    db = AsyncIOMotorClient(test_db, uuidRepresentation="standard")["weather_test"]
    await init_beanie(
        database=db,
        document_models=[User]
    )
    yield db

    await db.client.drop_database(db)

async def create_test_user():
    data = {
        "email": "test@example.com",
        "password": "password"
    }
    response = client.post("/api/v1/user/create", json=data)
    return response.json()

async def get_test_token(user: User):
    access_token = create_access_token(user.id)
    return access_token


async def get_test_user(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get("/api/v1/user/profile", headers=headers)
    return response.json()

@pytest.mark.asyncio
async def test_create_user(test_db):
    user = await create_test_user()
    assert user["email"] == "test@example.com"
    # Check that the user was saved in the database
    assert await User.get(user["_id"]) is not None

@pytest.mark.asyncio
async def test_get_me(test_db):
    user = await create_test_user()
    token = await get_test_token(user)
    me = await get_test_user(token)
    assert me["email"] == "test@example.com"
