from database.db import db
from services.category import CategoryService
from repositories.category import (
    CategoryQueryRepository, 
    CategoryCommandRepository
)

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_category_service(session: AsyncSession = Depends(db.get_session)):
    """Инжект сервиса категорий"""

    return CategoryService(
        query_repo=CategoryQueryRepository(session),
        command_repo=CategoryCommandRepository(session)
    )