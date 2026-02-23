from dateutil.relativedelta import relativedelta
from datetime import datetime, timezone

def get_period_start(period: str) -> datetime:
    now = datetime.now(timezone.utc)
    if period == 'day':
        return now - relativedelta(days=1)
    if period == 'week':
        return now - relativedelta(weeks=1)
    if period == 'month':
        return now - relativedelta(months=1)
    if period == 'year':
        return now - relativedelta(years=1)