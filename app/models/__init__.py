from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase, declared_attr


# 1. Define timestamp mixin
class TimestampMixin:
    """Mixin that adds created_at and updated_at to all models"""

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


# 2. Define your Base class here
class Base(DeclarativeBase, TimestampMixin):
    pass


# 3. Import all your models here
# This is CRITICAL for Alembic autogenerate to find your tables
from .stocks import Stock, DailyPrice, FinancialStatement, MarketEnum
