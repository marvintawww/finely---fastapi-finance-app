from models.token import TokenBlacklist

from sqlalchemy import select

class JWTQueryRepository:
    def __init__(self, session):
        self._session = session 
    
    async def get_by_jti(self, jti):
        stmt = select(TokenBlacklist).where(TokenBlacklist.jti == jti)
        result = await self._session.execute(stmt)
        token = result.scalar_one_or_none()
        return token
        

class JWTCommandRepository:
    def __init__(self, session):
        self._session = session
    
    async def add_to_blacklist(self, jti: str):
        try:
            token_bl = TokenBlacklist(jti=jti)
            self._session.add(token_bl)
            await self._session.commit()
            await self._session.refresh(token_bl)
            return token_bl
        except Exception:
            await self._session.rollback()
            raise