from utils.statistics import get_period_start
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta

class StatisticService:
    def __init__(self, query_repo):
        self.__query_repo = query_repo
        
    async def get_summary(self, user_id: int, period: str):
        date_from = get_period_start(period)
        income = await self.__query_repo.get_total_by_period(
            user_id=user_id,
            date_from=date_from,
            transaction_type='income'
        )
        expense = await self.__query_repo.get_total_by_period(
            user_id=user_id,
            date_from=date_from,
            transaction_type='expense'
        )
        balance = (income or 0.0) - (expense or 0.0)
        return {
            'income': income,
            'expense': expense,
            'balance': balance
        }
        
    async def get_month_compare(self, user_id: int):
        now = datetime.now(timezone.utc)

        current_month = now.replace(day=1)
        last_month_start = now.replace(day=1) - relativedelta(months=1)
        last_month_end = now.replace(day=1) - relativedelta(days=1)
        
        current_month_total_income = await self.__query_repo.get_total_by_period(
            user_id,
            date_from=current_month,
            transaction_type='income'
        )
        
        current_month_total_expense = await self.__query_repo.get_total_by_period(
            user_id,
            date_from=current_month,
            transaction_type='expense'
        )
        
        last_month_total_income = await self.__query_repo.get_total_by_period(
            user_id,
            date_from=last_month_start,
            date_to=last_month_end,
            transaction_type='income'
        )
        
        last_month_total_expense = await self.__query_repo.get_total_by_period(
            user_id,
            date_from=last_month_start,
            date_to=last_month_end,
            transaction_type='expense'
        )
        
        income_percent_compare = None
        expense_percent_compare = None
        
        if last_month_total_income:
            income_percent_compare = (float(current_month_total_income - last_month_total_income) / float(last_month_total_income)) * 100
            
        if last_month_total_expense:
            expense_percent_compare = (float(current_month_total_expense - last_month_total_expense) / float(last_month_total_expense)) * 100 
        
        return {
            'current_month_total_income': current_month_total_income or 0.0, 
            'current_month_total_expense': current_month_total_expense or 0.0, 
            'last_month_total_income': last_month_total_income or 0.0, 
            'last_month_total_expense': last_month_total_expense or 0.0, 
            'income_percent_compare': income_percent_compare or 0.0, 
            'expense_percent_compare': expense_percent_compare or 0.0, 
        }