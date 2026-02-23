from database.db import Base

from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

class TokenBlacklist(Base):
    __tablename__ = 'token_blacklist'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    jti: Mapped[str] = mapped_column(index=True)
    blacklisted_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))