"""
Модели базы данных
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Tariff(Base):
    __tablename__ = "tariffs"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, nullable=False)
    readings_count = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Связи
    users = relationship("User", back_populates="tariff")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String(32))
    first_name = Column(String(64))
    last_name = Column(String(64))
    language = Column(String(2), default="ru")
    readings_remaining = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    last_activity = Column(DateTime)
    
    # Реферальная система
    referral_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    referrals_count = Column(Integer, default=0)
    
    # Подписка
    subscription_end = Column(DateTime, nullable=True)
    tariff_id = Column(Integer, ForeignKey("tariffs.id"), nullable=True)
    
    # Связи
    readings = relationship("Reading", back_populates="user")
    payments = relationship("Payment", back_populates="user")
    referrals = relationship("User", backref="referrer", remote_side=[id])
    tariff = relationship("Tariff", back_populates="users")

class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question = Column(String(500), nullable=False)
    cards = Column(JSON, nullable=True)
    interpretation = Column(String(2000), nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Связи
    user = relationship("User", back_populates="readings")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="RUB")
    status = Column(String(20), default="pending")
    payment_id = Column(String(100), unique=True)
    created_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Связи
    user = relationship("User", back_populates="payments") 