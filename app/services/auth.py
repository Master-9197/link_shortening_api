from sqlalchemy import select
from passlib.context import CryptContext
from authx import AuthX, AuthXConfig
from datetime import timedelta
import os


from ..models.tables import *
from ..db.database import new_session
from ..schemas.user import UserCreate, UserBase


pass_mngr = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])


config = AuthXConfig()
config.JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
config.JWT_TOKEN_LOCATION = ["cookies"]
auth = AuthX(config=config)

AuthRequired = auth.access_token_required


class AuthService:
    @classmethod
    async def add_user(cls, user_data: UserCreate):
        async with new_session() as session:
            
            user_info = user_data.model_dump()

            hashed_password = pass_mngr.hash(user_data.password)
            user_info["hashed_password"] = hashed_password
            user_info.pop("password")

            user = Users(**user_info)
            session.add(user)
            await session.flush()
            await session.commit()
            return user.id
    
    
    @classmethod
    async def verify_user(cls, user_data: UserBase) -> str:
        async with new_session() as session:
            result = await session.execute(
                select(Users.hashed_password)
                .filter_by(login=user_data.login)
            )
            hashed_password = result.scalar()

            if pass_mngr.verify(secret=user_data.password,hash=hashed_password):
                result = await session.execute(
                    select(Users.id)
                    .filter_by(login=user_data.login)
                )

                user_id = result.scalar()

                access_token = auth.create_access_token(uid=str(user_id))

                return access_token
            
            else:
                raise 
                
