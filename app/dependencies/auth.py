from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

from config import SECRET
from database.db import db
from repositories.jwt import JWTQueryRepository
from utils.exceptions import (
    TokenDecodeError, 
    TokenBlaklistError, 
    TokenTypeError,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/')

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db.get_session)
) -> int:
    """Получение ID текущего юзера из токена

    Args:
        token (str, optional): Access-токен. Defaults to oauth2_scheme.

    Raises:
        TokenDecodeError: Ошибка декодинга токена
        TokenBlacklistError: Токен в черном списке

    Returns:
        int: ID текущего пользователя
    """
    
    try:
        payload = jwt.decode(token, SECRET, algorithms=['HS256'])
        repo = JWTQueryRepository(session)
        
        is_blacklisted = await repo.get_by_jti(payload.get('jti'))
        if is_blacklisted:
            raise TokenBlaklistError('Токен в черном списке')
        
        token_type = payload.get('type')
        if token_type != 'access':
            raise TokenTypeError('Неверный тип токена')
        
        user_id = int(payload.get('sub'))
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='JWT Ошибка'
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Срок действия подписи истек'
        )
    