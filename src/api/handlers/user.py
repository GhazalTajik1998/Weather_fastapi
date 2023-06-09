import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))




from fastapi import APIRouter, HTTPException, status
from schemas.user_schema import UserAuth, UserOut, UserUpdate
from fastapi import Depends
from services.user_service import UserService
import pymongo
from models.user_model import User
from api.dependency.user_deps import get_current_user


user_router = APIRouter()

@user_router.post('/create', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    try:
        return await UserService.create_user(data)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exist"
        )



@user_router.get('/profile', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: User = Depends(get_current_user)):
    return user

