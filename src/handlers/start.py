"""
Обработчики для команды /start
"""
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from keyboards.reply import get_main_keyboard
from database.models import User
from config import TAROT_SETTINGS
from handlers.question import QuestionStates

router = Router()

@router.message(F.text == "/start")
async def handle_start(message: types.Message, state: FSMContext, session: AsyncSession):
    """
    Обработчик команды /start
    """
    # Проверяем, существует ли пользователь
    user = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    )
    user = user.scalar_one_or_none()
    
    if not user:
        # Создаем нового пользователя
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language="ru",
            readings_remaining=TAROT_SETTINGS["free_readings_count"],
            is_active=True,
            created_at=datetime.utcnow()
        )
        session.add(user)
        await session.commit()
    
    # Устанавливаем начальное состояние
    await state.set_state(QuestionStates.main_menu)
    
    # Отправляем приветственное сообщение
    await message.answer(
        "Добро пожаловать в бота для гадания на картах Таро! "
        f"У вас есть {user.readings_remaining} бесплатных гаданий. "
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    ) 