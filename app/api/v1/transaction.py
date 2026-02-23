from fastapi import APIRouter, HTTPException, Depends, status
from datetime import date

from services.transaction import TransactionService
from schemas.transaction import TransactionCreate, TransactionResponse
from dependencies.auth import get_current_user
from dependencies.transaction import get_transaction_service
from utils.exceptions import TypeMatchError, NotFoundError

router = APIRouter(prefix='/api/v1/transactions')


@router.post(
    '/create',  
    response_model=TransactionResponse,
    status_code=status.HTTP_201_CREATED,
    summary='Создание транзакции'
)
async def new_transaction(
    data: TransactionCreate,
    user_id: int = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_transaction_service)
):
    """Создание новой транзакции

    Args:
        category_id: ID категории
        data: Данные о транзакции
        user_id: ID пользователя.
        transaction_service: Инжект сервиса транзакций.

    Returns:
        _type_: Транзакция
    """
    try:    
        transaction = await transaction_service.create_transaction(
            data=data,
            category_id=data.category_id,
            user_id=user_id
        )
    
        return transaction
    except TypeMatchError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Несовпадение типа транзакции/категории'
        )


@router.delete(
    '/{transaction_id}',
    status_code=status.HTTP_200_OK,
    summary='Удаление транзакции'
)
async def delete_transaction(
    transaction_id: int,
    user_id: int = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_transaction_service)
) -> dict:
    """Удаление транзакции

    Args:
        transaction_id: ID транзакции
        user_id: ID пользователя
        transaction_service: Инжект сервиса транзакций

    Raises:
        HTTPException: 
            404: Транзакция не найдена
            HTTP-ошибка

    Returns:
        dict: Сообщение о результате
    """
    
    try:
        await transaction_service.delete_transaction(transaction_id, user_id)
        return {'detail': 'Удаление транзакции успешно'}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Ошибка удаления'
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Транзакция не найдена'
        )
    

@router.get(
    '/',
    response_model=list[TransactionResponse],
    status_code=status.HTTP_200_OK,
    summary='Список всех транзакций'
)
async def get_all_transactions(
    user_id: int = Depends(get_current_user),
    search: str | None = None,
    transaction_type: str | None = None,
    category_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    order: str | None = 'desc',
    skip: int = 0,
    limit: int = 10,
    transaction_service: TransactionService = Depends(get_transaction_service)
) -> list:
    """Список всех транзакций

    Args:
        user_id: ID текущего пользователя
        search: query параметр для фильтрации
        transaction_type: query параметр для фильтрации
        category_id: query параметр для фильтрации
        skip: query параметр для пагинации
        limit: query параметр для пагинации
        transaction_service: Инжект сервиса транзакций

    Returns:
        list: Список транзакций
    """
    
    transactions = await transaction_service.get_transactions_list(
        user_id=user_id,
        search=search,
        transaction_type=transaction_type,
        category_id=category_id,
        date_from=date_from,
        date_to=date_to,
        order=order,
        skip=skip,
        limit=limit
    )
    
    return transactions


@router.get(
    '/{transaction_id}',
    response_model=TransactionResponse,
    status_code=status.HTTP_200_OK,
    summary='Получение одной транзакции'
)
async def get_one_transaction(
    transaction_id: int,
    user_id: int = Depends(get_current_user),
    transaction_service: TransactionService = Depends(get_transaction_service)
):
    """Получение одной транзакции

    Args:
        transaction_id: ID транзакции
        user_id (int, optional): ID текущего пользователя
        transaction_service: Инжект сервиса транзакций

    Raises:
        HTTPException: 404: Транзакция не найдена

    Returns:
        _type_: Транзакция
    """
    
    try:
        transaction = await transaction_service.get_transaction_by_id(
            user_id,
            transaction_id
        )
        return transaction
    except NotFoundError():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Транзакция не найдена'
        )
    
    