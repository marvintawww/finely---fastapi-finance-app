from database.db import db
from repositories.user import UserCommandRepository, UserQueryRepository
from services.user import UserService
from utils.security import PasswordHasher

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_user_service(session: AsyncSession = Depends(db.get_session)) -> UserService:
    """Инжект юзер сервиса"""
    return UserService(
        query_repo=UserQueryRepository(session),
        command_repo=UserCommandRepository(session),
        password_hasher=PasswordHasher()
    )