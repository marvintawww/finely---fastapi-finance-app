from schemas.category import (
    CategoryCreate, 
    CategoryCreateDB, 
    CategoryUpdate
)
from utils.exceptions import (
    CategoryExistingError, 
    DeleteError,
    CategoryNotFoundError,
    NotFoundError
)

class CategoryService:
    """Сервис категорий"""
    
    def __init__(self, query_repo, command_repo):
        self.__query_repo = query_repo
        self.__command_repo = command_repo
        
    async def create_category(self, data: CategoryCreate, user_id: int):
        """Создание категории

        Args:
            data (CategoryCreate): Данные для создания категории
            user_id (int): ID пользователя
        """
        
        existing = await self.__query_repo.get_by_name_and_id(
            name=data.name,
            user_id=user_id
        )
        
        if existing:
            raise CategoryExistingError('Категория уже существует')
        
        category_data = CategoryCreateDB(
            name=data.name,
            category_type=data.category_type,
            user_id=user_id
        )
        
        new_category = await self.__command_repo.create(category_data)
        return new_category
    
    async def delete_category(self, category_id: int, user_id: int) -> bool:
        """Удаление категории по ID

        Args:
            category_id (int): ID категории
        
        Raises:
            DeleteError: Ошибка при удалении    
            
        Returns:
            bool: True или False в зависимости от результата
        """
        try:
            result = await self.__command_repo.delete(category_id, user_id)
            return result
        except Exception:
            raise DeleteError('Ошибка при удалении категории')
    
    async def get_category_by_user(self, category_id: int, user_id: int):
        """Получить категорию по ID

        Args:
            category_id (int): ID категории

        Returns:
            _type_: Категория
        """
        
        category = await self.__query_repo.get_by_user_id(
            category_id=category_id,
            user_id=user_id
        )
        
        if category is None:
            raise CategoryNotFoundError('Категория не найдена')

        return category
    
    async def get_categories(
        self, 
        user_id: int, 
        search: str | None = None,
        category_type: str | None = None,
        skip: int = 0, 
        limit: int = 10,
    ):
        """Получение категорий

        Args:
            user_id (int): ID текущего пользователя
            search (str | None): Тектстовый поиск
            category_type (str | None): Тип категории
            skip (int, optional): skip параметр. Defaults to 0.
            limit (int, optional): limit параметр. Defaults to 10.

        Returns:
            _type_: Список категорий
        """
        
        categories = await self.__query_repo.get_categories_list(
            user_id=user_id,
            skip=skip,
            limit=limit,
            search=search,
            category_type=category_type
        )
        return categories
    
    async def category_update(
        self,
        data: CategoryUpdate,
        user_id: int,
        category_id: int
    ):
        """Обновление категории

        Args:
            data: Новые данные
            user_id: ID текущего пользователя
            category_id: ID категории

        Returns:
            _type_: Категорию
        """
        
        category = await self.__command_repo.category_update(
            data,
            user_id,
            category_id
        )
        return category