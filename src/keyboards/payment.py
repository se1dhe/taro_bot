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

def get_payment_menu(user) -> InlineKeyboardMarkup:
    """Клавиатура с тарифами"""
    builder = InlineKeyboardBuilder()
    
    # Добавляем тарифы
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
    # Добавляем кнопку для получения бесплатных раскладов
    builder.row(
        InlineKeyboardButton(
            text="🎁 Получить расклады бесплатно",
            callback_data="get_free_readings"
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

def get_referral_info_keyboard(user) -> InlineKeyboardMarkup:
    """Клавиатура с информацией о рефералах"""
    builder = InlineKeyboardBuilder()
    
    # Кнопка для возврата к тарифам
    builder.row(
        InlineKeyboardButton(
            text="⬅️ Назад к тарифам",
            callback_data="back_to_tariffs"
        )
    )
    
    return builder.as_markup() 