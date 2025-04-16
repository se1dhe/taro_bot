from aiogram import Router, types
from aiogram.filters import Text
from src.config import MONTHLY_READING_PROMPT_RU, MONTHLY_READING_PROMPT_EN, WEBAPP_URL
from src.database.models import User
from src.openai_client import get_openai_response
from data.tarot_cards import TAROT_CARDS
import json
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(Text("📅 Расклад на месяц"))
async def handle_monthly_reading(message: types.Message):
    user = await User.get_or_create(telegram_id=message.from_user.id)
    if not user.is_subscribed:
        await message.answer("Для использования этой функции необходима подписка. Пожалуйста, приобретите подписку.")
        return

    await message.answer(
        "Нажмите на кнопку ниже, чтобы открыть расклад на месяц",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Открыть расклад",
                        web_app=types.WebAppInfo(url=f"{WEBAPP_URL}/monthly_reading")
                    )
                ]
            ]
        )
    )

@router.message(lambda message: message.web_app_data and "monthly_reading" in message.web_app_data.url)
async def handle_monthly_reading_selection(message: types.Message):
    try:
        data = json.loads(message.web_app_data.data)
        selected_cards = data.get("selected_cards", [])
        
        if len(selected_cards) != 6:
            await message.answer("Пожалуйста, выберите 6 карт для расклада.")
            return

        # Получаем информацию о выбранных картах
        cards_info = []
        for card_id in selected_cards:
            card = TAROT_CARDS.get(str(card_id))
            if card:
                cards_info.append(f"{card['name']}: {card['description']}")

        # Формируем промт для GPT
        prompt = f"{MONTHLY_READING_PROMPT_RU}\n\nВыбранные карты:\n" + "\n".join(cards_info)

        # Получаем ответ от GPT
        response = await get_openai_response(prompt)
        
        # Отправляем ответ пользователю
        await message.answer(response)

    except Exception as e:
        logger.error(f"Ошибка при обработке расклада на месяц: {e}")
        await message.answer("Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже.") 