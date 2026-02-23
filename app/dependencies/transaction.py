from database.db import db
from services.transaction import TransactionService
from services.category import CategoryService
from dependencies.category import get_category_service
from repositories.transaction import (
    TransactionQueryRepository,
    TransactionCommandRepository
)

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_transaction_service(
    session: AsyncSession = Depends(db.get_session),
    category_service: CategoryService = Depends(get_category_service)
) -> TransactionService:
    """Инжект сервиса транзакций

    Args:
        session: Сессия БД.

    Returns:
        Сервис транзакций
    """
    
    return TransactionService(
        query_repo=TransactionQueryRepository(session),
        command_repo=TransactionCommandRepository(session),
        category_service=category_service
    )