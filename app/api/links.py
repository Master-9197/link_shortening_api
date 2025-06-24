from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError


from ..schemas.user import AddUserResponce, UserBase, UserCreate
from ..services.auth import AuthService


router = APIRouter(
    prefix="/api",
    tags=["Авторизация"]
)


@router.post("/register")
async def add_user(user_data: Annotated[UserCreate, Depends()]) -> AddUserResponce:
    try:
        user_id = await AuthService.add_user(user_data)
    except IntegrityError:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="This login is already in use")
    return {"ok": True, "user_id": user_id}


@router.get("/auth")
async def verify(
    user_data: Annotated[UserBase ,Depends()]):
    try:
        result = await AuthService.verify_user(user_data)

        return {"access_token": result}

    except Exception as e:
        print(f"ERROR verify - {e}")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)