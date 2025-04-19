from aiogram import Router, types, F
from src.config import MONTHLY_READING_PROMPT_RU, WEBAPP_URL
from src.database.models import User
from src.openai_client import get_openai_response
import json
import logging
import os
from aiogram.types import WebAppInfo
from keyboards.reply import get_main_keyboard

router = Router()
logger = logging.getLogger(__name__)

# Путь к директории с изображениями
IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'webapp', 'static', 'images')

@router.message(F.text == "📅 Расклад на месяц")
async def handle_monthly_reading(message: types.Message):
    logger.info("=============================")
    logger.info("========= ВЕРСИЯ: 2 =========")
    logger.info("=============================")
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

@router.message(lambda message: message.web_app_data is not None)
async def handle_monthly_reading_selection(message: types.Message) -> None:
    """Обработчик выбора карт для месячного расклада."""
    try:
        logger.info("Получены данные от веб-приложения")
        data = json.loads(message.web_app_data.data)
        logger.info(f"Полученные данные: {data}")
        logger.info(f"Тип данных: {type(data)}")
        logger.info(f"Длина данных: {len(data) if isinstance(data, (list, dict)) else 'не список/словарь'}")
        logger.info(f"Структура данных: {json.dumps(data, indent=2)}")
        
        if not isinstance(data, list):
            logger.error(f"Ожидался список, получен {type(data)}")
            await message.answer("Ошибка формата данных. Пожалуйста, попробуйте снова.")
            return
            
        cards_info = []
        cards_images = []
        
        for i, card_data in enumerate(data):
            logger.info(f"Обработка карты {i + 1}: {card_data}")
            logger.info(f"Тип данных карты: {type(card_data)}")
            
            if not isinstance(card_data, dict):
                logger.error(f"Ожидался словарь для карты {i + 1}, получен {type(card_data)}")
                continue
                
            try:
                path = card_data['path']
                is_reversed = card_data.get('isReversed', False)
            except KeyError as e:
                logger.error(f"Отсутствует обязательное поле {e} для карты {i + 1}")
                continue
            
            logger.info(f"Путь к карте: {path}, Перевернута: {is_reversed}")
            
            if not path:
                logger.error(f"Путь к карте не найден для карты {i + 1}")
                continue
                
            # Извлекаем информацию о карте из пути
            parts = path.split('/')
            if 'major' in path:
                card_number = int(parts[-1].split('.')[0])
                card_info = f"Старший аркан {card_number}"
                if is_reversed:
                    card_info += " (перевернутая)"
            else:
                suit = parts[-2]  # cups, wands, etc.
                card_number = int(parts[-1].split('.')[0])
                card_info = f"{suit.capitalize()} {card_number}"
                if is_reversed:
                    card_info += " (перевернутая)"
            
            cards_info.append(card_info)
            
            # Формируем абсолютный путь к изображению
            image_path = os.path.join(IMAGES_DIR, *parts[2:])  # Пропускаем 'static/images'
            cards_images.append(image_path)
            logger.info(f"Добавлена карта: {card_info}")
            logger.info(f"Полный путь к изображению: {image_path}")

        if not cards_info:
            logger.error("Не удалось получить информацию о картах")
            await message.answer("Не удалось получить информацию о картах. Пожалуйста, попробуйте снова.")
            return

        logger.info(f"Собранная информация о картах: {cards_info}")
        logger.info(f"Пути к изображениям: {cards_images}")

        # Формируем промт для GPT
        prompt = f"{MONTHLY_READING_PROMPT_RU}\n\nВыбранные карты:\n" + "\n".join(cards_info)
        logger.info(f"Сформированный промт: {prompt}")

        # Получаем ответ от GPT
        response = await get_openai_response(prompt)
        logger.info("Получен ответ от GPT")
        
        # Отправляем результат пользователю
        message_text = (
            f"🔮 Ваш месячный расклад:\n\n"
            f"Выбранные карты:\n" + "\n".join([f"• {card}" for card in cards_info]) +
            f"\n\n📝 Интерпретация:\n\n{response}"
        )
        
        logger.info("Отправка результата пользователю")
        
        # Отправляем текстовое сообщение
        await message.answer(
            message_text,
            reply_markup=get_main_keyboard()
        )
        
        # Отправляем изображения карт
        for image_path in cards_images:
            try:
                logger.info(f"Отправка изображения: {image_path}")
                if not os.path.exists(image_path):
                    logger.error(f"Файл не найден: {image_path}")
                    continue
                with open(image_path, 'rb') as photo:
                    await message.answer_photo(photo)
            except Exception as e:
                logger.error(f"Ошибка при отправке изображения {image_path}: {e}")
        
    except Exception as e:
        logger.error(f"Ошибка при обработке данных веб-приложения: {e}", exc_info=True)
        await message.answer(
            "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте снова.",
            reply_markup=get_main_keyboard()
        )