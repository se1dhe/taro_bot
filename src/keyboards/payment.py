"""
Клавиатуры для оплаты
"""
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import (
    TARIFF_SMALL_PRICE_STARS, TARIFF_SMALL_READINGS,
    TARIFF_MEDIUM_PRICE_STARS, TARIFF_MEDIUM_READINGS,
    TARIFF_UNLIMITED_PRICE_STARS
)

def get_payment_menu() -> InlineKeyboardMarkup:
    """Клавиатура с тарифами"""
    builder = InlineKeyboardBuilder()
    
    builder.row(
        InlineKeyboardButton(
            text=f"Тариф 'Малый' - {TARIFF_SMALL_PRICE_STARS} ⭐️",
            callback_data="buy_small"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Тариф 'Средний' - {TARIFF_MEDIUM_PRICE_STARS} ⭐️",
            callback_data="buy_medium"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Тариф 'Безлимитный' - {TARIFF_UNLIMITED_PRICE_STARS} ⭐️",
            callback_data="buy_unlimited"
        )
    )
    
    return builder.as_markup()

def get_payment_methods_keyboard(payment_id: str, tariff: str, robokassa_url: str) -> InlineKeyboardMarkup:
    """Клавиатура с методами оплаты"""
    builder = InlineKeyboardBuilder()
    
    # Кнопка для оплаты звёздами
    builder.row(
        InlineKeyboardButton(
            text="⭐️ Оплатить звёздами",
            callback_data=f"pay_stars_{tariff}_{payment_id}"
        )
    )
    
    # Кнопка для оплаты через Robokassa
    builder.row(
        InlineKeyboardButton(
            text="💳 Оплатить картой",
            url=robokassa_url
        )
    )
    
    return builder.as_markup() 