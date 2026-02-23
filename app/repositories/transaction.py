from sqlalchemy import select, and_, func, asc, desc
from datetime import date, datetime, timezone
from dateutil.relativedelta import relativedelta

from repositories.base import BaseCommandRepository, BaseQueryRepository
from models.transaction import Transaction
from schemas.transaction import TransactionCreateDB
from utils.exceptions import NotFoundError

class TransactionQueryRepository(BaseQueryRepository[Transaction]):
    """Transaction репо для запросов

    Args:
        BaseQueryRepository (_type_): Родительский репо
    """
    
    def __init__(self, session):
        super().__init__(session, Transaction)
        
    async def get_by_id(self, user_id: int, transaction_id: int) -> Transaction | None:
        """Получение транзакции

        Args:
            transaction_id: ID транзакции
            user_id (int): ID текущего пользователя

        Returns:
            Transaction | None
        """
        
        stmt = select(Transaction).where(
            and_(
                Transaction.user_id == user_id,
                Transaction.id == transaction_id
            )
        )
        result = await self._session.execute(stmt)
        transaction = result.scalar_one_or_none()
        return transaction
    
    async def get_transactions_list(
        self,
        user_id: int,
        search: str | None = None,
        transaction_type: str | None = None,
        category_id: int | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        order: str | None = 'desc',
        skip: int = 0,
        limit: int = 10
    ):
        """Список всех транзакций

        Args:
            user_id (int): _description_
            search (str | None, optional): _description_. Defaults to None.
            transaction_type (str | None, optional): _description_. Defaults to None.
            category_id (int | None, optional): _description_. Defaults to None.
            date_from (date | None, optional): _description_. Defaults to None.
            date_to (date | None, optional): _description_. Defaults to None.
            order (str | None, optional): _description_. Defaults to 'desc'.
            skip (int, optional): _description_. Defaults to 0.
            limit (int, optional): _description_. Defaults to 10.

        Returns:
            _type_: _description_
        """
        
        # TODO: написать docstring
        
        stmt = select(Transaction).where(
            Transaction.user_id == user_id
        )
        
        if search:
            stmt = stmt.where(
                func.lower(Transaction.name).contains(search.lower())
            )
            
        if transaction_type:
            stmt = stmt.where(
                Transaction.transaction_type == transaction_type
            )
            
        if category_id:
            stmt = stmt.where(
                Transaction.category_id == category_id
            )
            
        if date_from:
            stmt = stmt.where(
                Transaction.created_at >= date_from
            )
            
        if date_to:
            stmt = stmt.where(
                Transaction.created_at <= date_to
            )
            
        order_func = desc if order == 'desc' else asc
        
        stmt = stmt.order_by(
            order_func(Transaction.created_at)
        )    
            
        stmt = stmt.offset(skip).limit(limit)    
        transactions = await self._session.execute(stmt)
        return transactions.scalars().all()
    
    async def get_total(self, user_id: int, transaction_type: int):
        """Получить сумму транзакций одного типа

        Args:
            user_id: ID текущего пользователя
            transaction_type: Тип транзакции

        Returns:
            float: Сумма транзакций или 0.0
        """
        
        stmt = select(func.sum(Transaction.amount)).where(
            and_(
                Transaction.user_id == user_id,
                Transaction.transaction_type == transaction_type
            )
        )
        
        result = await self._session.execute(stmt)
        total = result.scalar_one_or_none()
        return total or 0.0
    
    async def get_total_by_period(
        self, 
        user_id: int, 
        date_from: datetime | None = None,
        date_to: datetime | None = None,
        transaction_type: str | None = None
    ):
        stmt = select(func.sum(Transaction.amount)).where(Transaction.user_id == user_id)
        
        if date_from:
            stmt = stmt.where(Transaction.created_at >= date_from)
            
        if date_to:
            stmt = stmt.where(Transaction.created_at <= date_to)
        
        if transaction_type:
            stmt = stmt.where(Transaction.transaction_type == transaction_type)
        
        result = await self._session.execute(stmt)
        total_by_period = result.scalar_one_or_none()
        return total_by_period

class TransactionCommandRepository(BaseCommandRepository[Transaction, TransactionCreateDB]):
    
    def __init__(self, session):
        super().__init__(session, Transaction)
        
    async def delete(
        self,
        transaction_id: int,
        user_id: int
    ):
        stmt = select(Transaction).where(
            and_(
                Transaction.id == transaction_id,
                Transaction.user_id == user_id
            )
        )
        result = await self._session.execute(stmt)
        transaction = result.scalar_one_or_none()
        if transaction is None:
            raise NotFoundError('Транзакция не найдена')
        try:
            await self._session.delete(transaction)
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise