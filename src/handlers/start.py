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
from config import TAROT_SETTINGS, BOT_USERNAME
from handlers.question import QuestionStates

router = Router()

@router.message(F.text.startswith("/start"))
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
        # Получаем реферальный ID из аргументов команды
        args = message.text.split()
        referral_id = None
        if len(args) > 1:
            try:
                referral_id = int(args[1])
            except ValueError:
                pass
        
        # Проверяем существование реферера
        referrer = None
        if referral_id:
            referrer = await session.execute(
                select(User).where(User.id == referral_id)
            )
            referrer = referrer.scalar_one_or_none()
        
        # Создаем нового пользователя
        user = User(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language="ru",
            readings_remaining=TAROT_SETTINGS["free_readings_count"],
            is_active=True,
            created_at=datetime.utcnow(),
            referral_id=referrer.id if referrer else None
        )
        session.add(user)
        await session.commit()
        
        # Если есть реферер, увеличиваем его счетчик рефералов
        if referrer:
            referrer.referrals_count += 1
            # Начисляем бонусные гадания рефереру
            referrer.readings_remaining += TAROT_SETTINGS["referral_bonus_readings"]
            await session.commit()
            
            # Отправляем уведомление рефереру
            try:
                await message.bot.send_message(
                    referrer.telegram_id,
                    f"🎉 У вас новый реферал! @{message.from_user.username or message.from_user.first_name} "
                    f"зарегистрировался по вашей ссылке. Вам начислено {TAROT_SETTINGS['referral_bonus_readings']} "
                    "бонусных гаданий!"
                )
            except Exception as e:
                print(f"Не удалось отправить уведомление рефереру: {e}")
    
    # Устанавливаем начальное состояние
    await state.set_state(QuestionStates.main_menu)
    
    # Отправляем приветственное сообщение
    welcome_text = (
        "Добро пожаловать в бота для гадания на картах Таро! "
        f"У вас есть {user.readings_remaining} бесплатных гаданий.\n\n"
        "Пригласите друзей и получите бонусные гадания! "
        f"Ваша реферальная ссылка: https://t.me/{BOT_USERNAME}?start={user.id}"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard()
    ) 