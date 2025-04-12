"""
Обработчик платежей
"""
from aiogram import Router, types
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import User, Payment
from config import (
    TARIFF_SMALL_PRICE,
    TARIFF_SMALL_READINGS,
    TARIFF_SMALL_DURATION,
    TARIFF_MEDIUM_PRICE,
    TARIFF_MEDIUM_READINGS,
    TARIFF_MEDIUM_DURATION,
    TARIFF_UNLIMITED_PRICE,
    TARIFF_UNLIMITED_DURATION
)

router = Router()

@router.callback_query(lambda c: c.data.startswith('tariff_'))
async def process_tariff_selection(callback_query: types.CallbackQuery, session: AsyncSession):
    tariff = callback_query.data.split('_')[1]
    
    # Получаем пользователя
    user = await session.execute(
        select(User).where(User.telegram_id == callback_query.from_user.id)
    )
    user = user.scalar_one_or_none()
    
    if not user:
        await callback_query.answer("Пожалуйста, сначала нажмите /start")
        return
    
    # Создаем платеж
    payment = Payment(
        user_id=user.id,
        amount=get_tariff_price(tariff),
        status='pending',
        tariff=tariff,
        created_at=datetime.utcnow()
    )
    
    session.add(payment)
    await session.commit()
    
    # TODO: Добавить логику оплаты через Robokassa
    await callback_query.answer("Платеж создан. Скоро добавим оплату через Robokassa.")

def get_tariff_price(tariff: str) -> int:
    """Возвращает цену тарифа"""
    if tariff == 'small':
        return TARIFF_SMALL_PRICE
    elif tariff == 'medium':
        return TARIFF_MEDIUM_PRICE
    elif tariff == 'unlimited':
        return TARIFF_UNLIMITED_PRICE
    else:
        raise ValueError(f"Unknown tariff: {tariff}") 