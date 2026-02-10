from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, Date, DateTime, func, Integer, Text, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class Transaction(Base):
    __tablename__ = "cost_transactions"

    transaction_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    transaction_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    cost_center: Mapped[str] = mapped_column(String(100), nullable=False)
    receiver_cost_center: Mapped[str] = mapped_column(String(100), nullable=False)
    cost_object: Mapped[str] = mapped_column(String(100), nullable=False)
    cost_type: Mapped[str] = mapped_column(String(10), nullable=False)
    __table_args__ = (
        CheckConstraint(cost_type.in_(['Internal', 'External']), name='check_cost_type'),
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)

class CalculationTask(Base):
    __tablename__ = "calculation_tasks"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    target_month: Mapped[datetime.date] = mapped_column(Date, unique=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    error_message: Mapped[str] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

class AllocatedCost(Base):
    __tablename__ = "cost_center_allocated"
    
    month: Mapped[datetime.date] = mapped_column(Date, primary_key=True)
    cost_center: Mapped[str] = mapped_column(String(100), primary_key=True)
    total_cost: Mapped[Decimal] = mapped_column(Numeric(14, 2))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())