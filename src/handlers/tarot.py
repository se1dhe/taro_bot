from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from src.config import TAROT_SETTINGS, WEBAPP_URL
from src.utils.tarot import get_random_tarot_cards

router = Router()

@router.message(Command("tarot"))
async def handle_tarot(message: Message, user: User) -> None:
    """Обработчик команды /tarot"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Выбрать карты",
                    web_app={"url": f"{WEBAPP_URL}/tarot"}
                )
            ]
        ]
    )
    
    await message.answer(
        "Нажмите на кнопку ниже, чтобы открыть мини-приложение для выбора карт Таро:",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "tarot_reading")
async def handle_tarot_reading(callback: CallbackQuery, user: User, session: AsyncSession) -> None:
    """Обработчик нажатия на кнопку гадания"""
    if user.readings_remaining <= 0:
        await callback.message.answer(
            "У вас нет доступных гаданий. Пожалуйста, приобретите подписку."
        )
        return

    # Получаем случайные карты
    cards = get_random_tarot_cards()
    
    # Обновляем количество оставшихся гаданий
    user.readings_remaining -= 1
    await session.commit()
    
    # Отправляем сообщение с картами
    await callback.message.answer(
        f"Ваши карты:\n\n"
        f"1. {cards[0]}\n"
        f"2. {cards[1]}\n"
        f"3. {cards[2]}\n\n"
        f"Осталось гаданий: {user.readings_remaining}"
    ) 