from database.db import db
from services.statistics import StatisticService
from repositories.transaction import TransactionQueryRepository

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

async def get_statistics_service(session: AsyncSession = Depends(db.get_session)):
    return StatisticService(
        query_repo=TransactionQueryRepository(session)
    )