from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

from config import DATABASE_URL

class Database:
    """База данных"""
    
    def __init__(self, url: str):
        self.__engine = create_async_engine(
            url, echo=True
        )
        self.__session = async_sessionmaker(
            bind=self.__engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False
        )
        self.__Base = declarative_base()
        
    async def get_session(self):
        """Сессия БД

        Yields:
            _type_: Дает сессию БД
        """
        async with self.__session() as session:
            try:
                yield session
            finally:
                session.close()
    
    async def create_tables(self):
        """Создание таблиц"""
        async with self.__engine.begin() as conn:
            await conn.run_sync(self.__Base.metadata.create_all)
    
    async def drop_tables(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(self.__Base.metadata.drop_all)
            
    @property
    def engine(self):
        return self.__engine
    
    @property
    def base(self):
        return self.__Base
    
    
db = Database(DATABASE_URL)
Base = db.base