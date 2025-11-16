import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum,
    Float,
    Date,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from . import Base  # Import Base from app/models/__init__.py

# --- Enum for Market Choices ---


class MarketEnum(enum.Enum):
    KOSPI = "KOSPI"
    KOSDAQ = "KOSDAQ"


# --- Stock Model ---


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    market = Column(Enum(MarketEnum), nullable=False)
    ticker = Column(String(10), unique=True, index=True, nullable=False)

    no_fs = Column(Boolean, default=True)
    fs_score = Column(Integer, default=0)
    vcp_score = Column(Integer, default=0)

    trend_template_passed = Column(Boolean, default=False)

    # Relationships
    daily_prices = relationship(
        "DailyPrice", back_populates="stock", cascade="all, delete-orphan"
    )
    financial_statements = relationship(
        "FinancialStatement", back_populates="stock", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Stock(name='{self.name}', ticker='{self.ticker}')>"


# --- DailyPrice Model ---


class DailyPrice(Base):
    __tablename__ = "daily_prices"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)

    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    stock = relationship("Stock", back_populates="daily_prices")

    # Technical Indicators
    ma_50 = Column(Float, nullable=True)
    ma_150 = Column(Float, nullable=True)
    ma_200 = Column(Float, nullable=True)
    ma_200_20d_ago = Column(Float, nullable=True)
    is_ma_200_bullish = Column(Boolean, nullable=True)

    week_52_high = Column(Float, nullable=True)
    is_near_week_52_high = Column(Boolean, nullable=True)
    week_52_low = Column(Float, nullable=True)
    is_above_week_52_low_threshold = Column(Boolean, nullable=True)

    roc_252 = Column(Float, nullable=True)
    roc_126 = Column(Float, nullable=True)
    roc_63 = Column(Float, nullable=True)
    roc_21 = Column(Float, nullable=True)

    rs_momentum = Column(Float, nullable=True)
    rs_rank = Column(Integer, nullable=True)
    rs_grade = Column(Float, nullable=True)

    __table_args__ = (
        UniqueConstraint("stock_id", "date", name="_stock_date_uc"),
        Index("ix_daily_prices_stock_id_date", "stock_id", "date"),
        Index("ix_daily_prices_date", "date"),
    )


# --- FinancialStatement Model ---


class FinancialStatement(Base):
    __tablename__ = "financial_statements"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    quarter = Column(Integer, nullable=False)

    revenue = Column(Float)
    operating_income = Column(Float)
    net_income = Column(Float)

    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    stock = relationship("Stock", back_populates="financial_statements")

    # Revenue flags
    is_revenue_better_than_tm1_quarter = Column(Boolean, default=False)
    is_revenue_tm1_quarter_better_than_tm2_quarter = Column(Boolean, default=False)
    is_revenue_tm2_quarter_better_than_tm3_quarter = Column(Boolean, default=False)
    is_revenue_this_year_better_than_last_year = Column(Boolean, default=False)
    is_revenue_this_quarter_better_than_year_before_quarter = Column(
        Boolean, default=False
    )

    revenue_growth_rate_this_quarter = Column(Float, default=0)
    revenue_growth_rate_tm1_quarter = Column(Float, default=0)
    revenue_growth_rate_tm2_quarter = Column(Float, default=0)
    revenue_growth_rate_tm3_quarter = Column(Float, default=0)

    is_revenue_growth_rate_better_than_tm1_growth_rate = Column(Boolean, default=False)
    is_revenue_growth_rate_better_than_tm2_growth_rate = Column(Boolean, default=False)
    is_revenue_growth_rate_better_than_tm3_growth_rate = Column(Boolean, default=False)

    # Operating Income flags
    is_operating_income_better_than_tm1_quarter = Column(Boolean, default=False)
    is_operating_income_tm1_quarter_better_than_tm2_quarter = Column(
        Boolean, default=False
    )
    is_operating_income_tm2_quarter_better_than_tm3_quarter = Column(
        Boolean, default=False
    )
    is_operating_income_this_year_better_than_last_year = Column(Boolean, default=False)
    is_oi_this_quarter_better_than_year_before_quarter = Column(Boolean, default=False)

    operating_income_growth_rate_this_quarter = Column(Float, default=0)
    operating_income_growth_rate_tm1_quarter = Column(Float, default=0)
    operating_income_growth_rate_tm2_quarter = Column(Float, default=0)
    operating_income_growth_rate_tm3_quarter = Column(Float, default=0)

    is_operating_income_growth_rate_better_than_tm1_growth_rate = Column(
        Boolean, default=False
    )
    is_operating_income_growth_rate_better_than_tm2_growth_rate = Column(
        Boolean, default=False
    )
    is_operating_income_growth_rate_better_than_tm3_growth_rate = Column(
        Boolean, default=False
    )

    __table_args__ = (
        UniqueConstraint("stock_id", "year", "quarter", name="_stock_year_quarter_uc"),
        Index("ix_fs_stock_id_year_quarter", "stock_id", "year", "quarter"),
    )
