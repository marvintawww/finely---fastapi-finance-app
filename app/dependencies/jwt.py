from database.db import db
from repositories.jwt import JWTCommandRepository, JWTQueryRepository
from services.jwt import JWTService

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_jwt_service(session: AsyncSession = Depends(db.get_session)):
    """Получение JWTService

    Args:
        session (AsyncSession, optional): БД сыессия. Defaults to Depends(db.get_session).

    Returns:
        _type_: JWTService
    """
    
    return JWTService(
        query_repo=JWTQueryRepository(session),
        command_repo=JWTCommandRepository(session)
    )
