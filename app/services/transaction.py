from schemas.transaction import TransactionCreate, TransactionCreateDB
from utils.exceptions import NotFoundError, TypeMatchError

from datetime import date

class TransactionService:
    
    def __init__(self, query_repo, command_repo, category_service):
        self.__query_repo = query_repo
        self.__command_repo = command_repo
        self.__category_service = category_service
        
    async def create_transaction(self, 
        data: TransactionCreate, 
        category_id: int, 
        user_id: int
    ):
        """Создание транзакции

        Args:
            data: Данные о транзакции
            category_id: ID категории
            user_id: ID пользователя
            category_type: Тип категории
        """
        
        category = await self.__category_service.get_category_by_user(
            category_id=category_id,
            user_id=user_id
        )
        
        if category.category_type != data.transaction_type:
            raise TypeMatchError('Несоответствие типа транзакции и категории')
        
        transaction_data = TransactionCreateDB(
            name=data.name,
            transaction_type=data.transaction_type,
            amount=data.amount,
            category_id=category_id,
            user_id=user_id
        )
        
        transaction = await self.__command_repo.create(transaction_data)
        return transaction
    
    async def delete_transaction(self, 
        transaction_id: int, 
        user_id: int
    ) -> bool:
        """Удаление транзакции

        Args:
            transaction_id (int): ID транзакции

        Returns:
            bool: True или False в зависимости от результата
        """
        
        result = await self.__command_repo.delete(transaction_id, user_id)
        return result
        
    async def get_transaction_by_id(self, user_id: int, transaction_id: int):
        """Получить транзакцию по ID

        Args:
            transaction_id (int): ID транзакции

        Returns:
            _type_: Транзакция
        """
        
        transaction = await self.__query_repo.get_by_id(user_id, transaction_id)
        if transaction is None:
            raise NotFoundError('Транзакция не найдена')
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
        """Получениие списка транзакций

        Args:
            user_id: ID текущего пользователя
            search: query параметр для фильтрации 
            transaction_type: query параметр для фильтрации
            category_id: query параметр для фильтрации
            skip: query параметр для пагинации
            limit: query параметр для пагинации

        Returns:
            _type_: Список транзакций
        """
        transactions = await self.__query_repo.get_transactions_list(
            user_id,
            search,
            transaction_type,
            category_id,
            date_from,
            date_to,
            order,
            skip,
            limit
        )
        return transactions