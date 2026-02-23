from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint

from database.db import Base

class Category(Base):
    __tablename__ = 'categories'
    
    __table_args__ = (UniqueConstraint('name', 'user_id'),)
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    category_type: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped["User"] = relationship("User", back_populates="categories")
    transactions: Mapped[list["Transaction"]] = relationship("Transaction", back_populates="category")