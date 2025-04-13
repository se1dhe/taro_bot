from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import (
    TARIFF_SMALL_PRICE, TARIFF_SMALL_READINGS,
    TARIFF_MEDIUM_PRICE, TARIFF_MEDIUM_READINGS,
    TARIFF_UNLIMITED_PRICE
)

def get_payment_menu() -> InlineKeyboardMarkup:
    """Создает меню оплаты с тарифами"""
    builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки с тарифами
    builder.row(InlineKeyboardButton(
        text=f"{TARIFF_SMALL_READINGS} расклада - {TARIFF_SMALL_PRICE}₽",
        callback_data=f"buy_small"
    ))
    
    builder.row(InlineKeyboardButton(
        text=f"{TARIFF_MEDIUM_READINGS} раскладов - {TARIFF_MEDIUM_PRICE}₽",
        callback_data=f"buy_medium"
    ))
    
    builder.row(InlineKeyboardButton(
        text=f"Безлимит на месяц - {TARIFF_UNLIMITED_PRICE}₽",
        callback_data=f"buy_unlimited"
    ))
    
    # Кнопка для получения бесплатных раскладов
    builder.row(InlineKeyboardButton(
        text="🚀 Получить расклады бесплатно",
        callback_data="get_free_readings"
    ))
    
    # Кнопка для оплаты через Telegram Stars
    builder.row(InlineKeyboardButton(
        text="⭐️ Оплата Telegram Stars",
        callback_data="pay_stars"
    ))
    
    return builder.as_markup() 