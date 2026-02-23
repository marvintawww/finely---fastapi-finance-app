from schemas.user import UserCreateDB
from models.user import User
from repositories.base import BaseCommandRepository, BaseQueryRepository

from sqlalchemy import select

class UserCommandRepository(BaseCommandRepository[User, UserCreateDB]):
    def __init__(self, session):
        super().__init__(session, User)


class UserQueryRepository(BaseQueryRepository[User]):
    def __init__(self, session):
        super().__init__(session, User)
        
    async def get_by_login(self, login: str) -> User | None:
        """Поиска пользователя по ИМЕНИ

        Args:
            name (str): INPUT-имя

        Returns:
            User | None: Если пользователь есть то возвращает его, если нет - None
        """
        
        stmt = select(User).where(User.login == login)
        result = await self._session.execute(stmt)
        user = result.scalar_one_or_none()
        return user
    
