#!/usr/bin/env python3
"""
PostgreSQL Database Models for Agent Chopra
Comprehensive data models for trading data, user profiles, and risk assessment
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from datetime import datetime
import uuid
import enum
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

# Database compatibility function
def get_uuid_column():
    """Return appropriate UUID column type based on database"""
    database_url = os.getenv('DATABASE_URL', '')
    if 'sqlite' in database_url.lower():
        # SQLite compatibility - use String instead of UUID
        return lambda: Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    else:
        # PostgreSQL UUID support
        from sqlalchemy.dialects.postgresql import UUID
        return lambda: Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

def get_uuid_foreign_key(table_column):
    """Return appropriate UUID foreign key type based on database"""
    database_url = os.getenv('DATABASE_URL', '')
    if 'sqlite' in database_url.lower():
        return Column(String(36), ForeignKey(table_column), nullable=False)
    else:
        from sqlalchemy.dialects.postgresql import UUID
        return Column(UUID(as_uuid=True), ForeignKey(table_column), nullable=False)

# Enums
class RiskLevel(enum.Enum):
    VERY_LOW = 1
    LOW = 2
    LOW_MODERATE = 3
    MODERATE = 4
    MODERATE_HIGH = 5
    HIGH = 6
    HIGH_AGGRESSIVE = 7
    AGGRESSIVE = 8
    VERY_AGGRESSIVE = 9
    EXTREME = 10

class OrderStatus(enum.Enum):
    PENDING = "pending"
    FILLED = "filled"
    CANCELED = "canceled"
    REJECTED = "rejected"
    PARTIALLY_FILLED = "partially_filled"

class OrderSide(enum.Enum):
    BUY = "buy"
    SELL = "sell"

class OrderType(enum.Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"

class Sector(enum.Enum):
    TECHNOLOGY = "technology"
    HEALTHCARE = "healthcare"
    FINANCIALS = "financials"
    CONSUMER_DISCRETIONARY = "consumer_discretionary"
    CONSUMER_STAPLES = "consumer_staples"
    ENERGY = "energy"
    UTILITIES = "utilities"
    INDUSTRIALS = "industrials"
    MATERIALS = "materials"
    REAL_ESTATE = "real_estate"
    TELECOMMUNICATIONS = "telecommunications"

# User Management
class User(Base):
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100))

    # Profile Information
    risk_profile = Column(SQLEnum(RiskLevel), default=RiskLevel.MODERATE)
    investment_experience = Column(String(20))  # beginner, intermediate, advanced, expert
    age_range = Column(String(20))  # 18-25, 26-35, etc.
    income_range = Column(String(20))  # <50k, 50k-100k, etc.
    investment_goals = Column(Text)

    # Account Settings
    alpaca_api_key = Column(String(255))
    alpaca_secret_key = Column(String(255))
    notifications_enabled = Column(Boolean, default=True)
    dark_mode = Column(Boolean, default=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    trades = relationship("Trade", back_populates="user")
    positions = relationship("Position", back_populates="user")
    risk_assessments = relationship("RiskAssessment", back_populates="user")
    portfolio_snapshots = relationship("PortfolioSnapshot", back_populates="user")
    ai_interactions = relationship("AIInteraction", back_populates="user")

# Trading Data
class Trade(Base):
    __tablename__ = 'trades'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    alpaca_order_id = Column(String(100), unique=True)

    # Order Details
    symbol = Column(String(10), nullable=False)
    side = Column(SQLEnum(OrderSide), nullable=False)
    order_type = Column(SQLEnum(OrderType), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Pricing
    limit_price = Column(Float)
    stop_price = Column(Float)
    filled_price = Column(Float)
    filled_quantity = Column(Integer, default=0)

    # Status and Timing
    status = Column(SQLEnum(OrderStatus), nullable=False)
    submitted_at = Column(DateTime, nullable=False)
    filled_at = Column(DateTime)

    # Performance Tracking
    unrealized_pnl = Column(Float)
    realized_pnl = Column(Float)

    # Metadata
    strategy_used = Column(String(50))
    risk_score = Column(Float)
    market_conditions = Column(JSON)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="trades")

class Position(Base):
    __tablename__ = 'positions'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Position Details
    symbol = Column(String(10), nullable=False)
    quantity = Column(Float, nullable=False)
    avg_entry_price = Column(Float, nullable=False)
    current_price = Column(Float)

    # Valuation
    market_value = Column(Float)
    cost_basis = Column(Float)
    unrealized_pnl = Column(Float)
    unrealized_pnl_percent = Column(Float)

    # Risk Metrics
    position_risk_score = Column(Float)
    sector = Column(SQLEnum(Sector))
    beta = Column(Float)

    # Timestamps
    opened_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    closed_at = Column(DateTime)

    # Relationships
    user = relationship("User", back_populates="positions")

# Risk Assessment and Profiling
class RiskAssessment(Base):
    __tablename__ = 'risk_assessments'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Assessment Details
    assessment_type = Column(String(50))  # initial, periodic, triggered
    risk_score = Column(Integer, nullable=False)  # 1-10
    risk_level = Column(SQLEnum(RiskLevel), nullable=False)

    # Assessment Components
    age_score = Column(Integer)
    income_score = Column(Integer)
    experience_score = Column(Integer)
    time_horizon_score = Column(Integer)
    risk_tolerance_score = Column(Integer)

    # Portfolio Analysis
    current_allocation = Column(JSON)
    recommended_allocation = Column(JSON)
    diversification_score = Column(Float)

    # Assessment Results
    summary = Column(Text)
    recommendations = Column(JSON)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="risk_assessments")

# Portfolio Snapshots
class PortfolioSnapshot(Base):
    __tablename__ = 'portfolio_snapshots'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Portfolio Metrics
    total_value = Column(Float, nullable=False)
    cash_balance = Column(Float, nullable=False)
    buying_power = Column(Float, nullable=False)
    day_trading_buying_power = Column(Float)

    # Performance Metrics
    total_pnl = Column(Float)
    total_pnl_percent = Column(Float)
    daily_pnl = Column(Float)
    positions_count = Column(Integer)

    # Risk Metrics
    portfolio_beta = Column(Float)
    sharpe_ratio = Column(Float)
    max_drawdown = Column(Float)
    value_at_risk = Column(Float)

    # Allocation Data
    sector_allocation = Column(JSON)
    position_sizes = Column(JSON)

    # Timestamps
    snapshot_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="portfolio_snapshots")

# AI Interactions and Insights
class AIInteraction(Base):
    __tablename__ = 'ai_interactions'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Interaction Details
    interaction_type = Column(String(50))  # chat, insight, recommendation, analysis
    user_query = Column(Text)
    ai_response = Column(Text)

    # Context Data
    portfolio_context = Column(JSON)
    market_context = Column(JSON)

    # Feedback
    user_rating = Column(Integer)  # 1-5 stars
    was_helpful = Column(Boolean)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="ai_interactions")

# Stock/Company Information
class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    # Basic Info
    symbol = Column(String(10), unique=True, nullable=False)
    company_name = Column(String(200))
    sector = Column(SQLEnum(Sector))
    industry = Column(String(100))

    # Risk Metrics
    risk_rating = Column(Integer)  # 1-10
    beta = Column(Float)
    volatility = Column(Float)
    market_cap = Column(Float)

    # Fundamental Data
    pe_ratio = Column(Float)
    dividend_yield = Column(Float)
    debt_to_equity = Column(Float)
    roe = Column(Float)

    # Technical Indicators
    price_trend = Column(String(20))  # uptrend, downtrend, sideways
    support_level = Column(Float)
    resistance_level = Column(Float)

    # AI Analysis
    ai_sentiment = Column(String(20))  # bullish, bearish, neutral
    recommendation = Column(String(20))  # buy, sell, hold
    target_price = Column(Float)

    # Timestamps
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Market Alerts and Notifications
class Alert(Base):
    __tablename__ = 'alerts'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)

    # Alert Details
    alert_type = Column(String(50))  # price, risk, portfolio, ai_insight
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String(20))  # low, medium, high, critical

    # Targeting
    symbol = Column(String(10))
    trigger_price = Column(Float)

    # Status
    is_active = Column(Boolean, default=True)
    is_read = Column(Boolean, default=False)
    triggered_at = Column(DateTime)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)

# Database Connection and Session Management
class DatabaseManager:
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        if not self.database_url:
            # Fallback to SQLite for development
            self.database_url = 'sqlite:///agent_chopra.db'

        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)

    def get_session(self):
        """Get a database session"""
        return self.SessionLocal()

    def close_session(self, session):
        """Close a database session"""
        session.close()

# Singleton instance
db_manager = DatabaseManager()

def get_db():
    """Dependency to get database session"""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db_manager.close_session(db)