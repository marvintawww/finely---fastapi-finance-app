from sqlalchemy import select, and_

from models.category import Category
from schemas.category import CategoryCreateDB, CategoryUpdate
from repositories.base import BaseCommandRepository, BaseQueryRepository
from utils.exceptions import NotFoundError


class CategoryQueryRepository(BaseQueryRepository[Category]):
    """Репо для работы с БД категорий (Запросы)

    Args:
        BaseQueryRepository (_type_): Родительский репо
    """
    
    def __init__(self, session):
        super().__init__(session, Category)
        
    async def get_by_user_id(self, category_id: int, user_id: int) -> Category | None:
        """Поиск категории по имени и ID пользователя

        Args:
            name (str): INPUT-имя
            user_id (int): INPUT-id

        Returns:
            Category | None: Категория, если найдена или None
        """
        
        stmt = select(Category).where(
            and_(
                Category.id == category_id, 
                Category.user_id == user_id
            )
        )
        result = await self._session.execute(stmt)
        category = result.scalar_one_or_none()
        return category
    
    async def get_by_name_and_id(self, 
        name: str, 
        user_id: int
    ) -> Category | None:
        """Поиск категории по названию и ID текущего пользователя

        Args:
            name: Название категории
            user_id: ID текущего пользователя

        Returns:
            Category | None: _description_
        """
        
        stmt = select(Category).where(
            and_(
                Category.name == name,
                Category.user_id == user_id
            )
        )
        
        result = await self._session.execute(stmt)
        category = result.scalar_one_or_none()
        return category
    
    async def get_categories_list(
        self, 
        user_id: int, 
        category_type: str | None = None,
        search: str | None = None,
        skip: int = 0, 
        limit: int = 10,
    ):
        """Список категорий с фильтрацией и пагинацией

        Args:
            user_id (int): ID текущего пользователя
            category_type (str | None): Тип категории
            search (str | None): Текстовый поиск
            skip (int, optional): skip параметр. Defaults to 0.
            limit (int, optional): limit параметр. Defaults to 10.

        Returns:
            _type_: Список категорий
        """
        
        stmt = select(Category).where(
            Category.user_id == user_id
        )
        
        if search:
            stmt = stmt.where(
                Category.name.ilike(f'%{search}%')
            )
        
        if category_type:
            stmt = stmt.where(
                Category.category_type == category_type
            )

        stmt = stmt.offset(skip).limit(limit)
        
        categories = await self._session.execute(stmt)
        return categories.scalars().all()


class CategoryCommandRepository(BaseCommandRepository[Category, CategoryCreateDB]):
    """Репо для работы с БД категорий (Комманды)

    Args:
        BaseCommandRepository (_type_): Родительский репо
    """
    
    def __init__(self, session):
        super().__init__(session, Category)
        
    async def delete(self, 
        category_id: int, 
        user_id: int
    ):
        """Удаление транзакции

        Args:
            category_id (int): ID категории
            user_id (int): ID пользователя

        Returns:
            _type_: (Success/Fail)
        """
        
        stmt = select(Category).where(
            and_(
                Category.id == category_id,
                Category.user_id == user_id
            )
        )
        result = await self._session.execute(stmt)
        category = result.scalar_one_or_none()
        if not category:
            return False
        try:
            await self._session.delete(category)
            await self._session.commit()
            return True
        except Exception:
            await self._session.rollback()
            raise
        
    async def category_update(
        self,
        data: CategoryUpdate,
        user_id: int,
        category_id: int
    ) -> Category:
        """Обновление информации о категории

        Args:
            data: Новые входные данные
            user_id: ID текущего пользователя
            category_id: ID категории

        Raises:
            NotFoundError: Категория не найдена

        Returns:
            Category: Обновленная категория
        """
        
        stmt = select(Category).where(
            and_(
                Category.user_id == user_id,
                Category.id == category_id
            )
        )
        
        result = await self._session.execute(stmt)
        category = result.scalar_one_or_none()
        if category is None:
            raise NotFoundError('Категория не найдена')
        
        update_data = data.model_dump(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(category, key, value)
            
        try:
            await self._session.commit()
            await self._session.refresh(category)
            return category
        except Exception:
            await self._session.rollback()
            raise