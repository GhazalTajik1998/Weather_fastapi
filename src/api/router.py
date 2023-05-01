import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi import APIRouter
from .handlers.user import user_router
from api.auth.jwt import auth_router
from .weather.weather_api import weather_router

router = APIRouter()

router.include_router(user_router, prefix="/users", tags=["users"])
router.include_router(auth_router, prefix='/auth', tags=["auth"])
router.include_router(weather_router, prefix='/weather', tags=["weather"])

