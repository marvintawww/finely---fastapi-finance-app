from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, ExpiredSignatureError

from dependencies.statistics import get_statistics_service
from dependencies.auth import get_current_user 
from services.statistics import StatisticService
from utils.tips import get_random_tip

router = APIRouter(prefix='/api/v1/statistics')

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    summary='Получить статистику'
)
async def get_stat(
    period: str | None = None,
    user_id: int = Depends(get_current_user),
    stat_service: StatisticService = Depends(get_statistics_service)
):  
    try:
        summary_stat = await stat_service.get_summary(
            user_id,
            period
        )
        
        compare = await stat_service.get_month_compare(user_id)
        
        return {
            'summary_stat': summary_stat,
            'month_compare': compare,
            'tip': get_random_tip()
        }
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Подпись истекла'
        )