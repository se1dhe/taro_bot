"""
Функции для работы с базой данных
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from .models import User

async def get_user(telegram_id: int, session: AsyncSession) -> Optional[User]:
    """Получение пользователя по telegram_id"""
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    return result.scalar_one_or_none()

async def update_user_readings(user_id: int, readings: int, session: AsyncSession) -> None:
    """Обновление количества раскладов у пользователя"""
    user = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = user.scalar_one_or_none()
    
    if user:
        user.readings_left = readings
        await session.commit() 