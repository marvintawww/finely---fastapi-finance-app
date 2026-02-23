from sqlalchemy import select
from typing import TypeVar, Generic, Type


T = TypeVar('T')
C = TypeVar('C')

class BaseQueryRepository(Generic[T]):
    """Родительский репо для запросов"""
    
    def __init__(self, session, model: Type[T]):
        self._session = session
        self._model = model
        
    async def get_by_id(self, id: int) -> T | None:
        stmt = select(self._model).where(self._model.id == id)
        result = await self._session.execute(stmt)
        obj = result.scalar_one_or_none()
        return obj
        

class BaseCommandRepository(Generic[T, C]):
    """Родительский репо для комманд"""
    
    def __init__(self, session, model: Type[T]):
        self._session = session
        self._model = model
        
    async def create(self, data: C) -> T:
        try:
            obj = self._model(**data.model_dump())
            self._session.add(obj)
            await self._session.commit()
            await self._session.refresh(obj)
            return obj
        except Exception:
            await self._session.rollback()
            raise
    
    async def delete(self, id: int) -> bool:
        try:
            stmt = select(self._model).where(self._model.id == id)
            result = await self._session.execute(stmt)
            obj = result.scalar_one_or_none()
            if not obj:
                return False
            await self._session.delete(obj)
            await self._session.commit()
            return True
        except Exception:
            await self._session.rollback()
            raise
        