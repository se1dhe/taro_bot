"""
Клавиатуры для бота
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает основную клавиатуру с главными действиями
    """
    keyboard = [
        [KeyboardButton(text="🎴 Задать вопрос")],
        [KeyboardButton(text="💳 Купить расклады")],
        [KeyboardButton(text="❓ Как работает бот")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_question_actions_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для действий после ввода вопроса
    """
    keyboard = [
        [KeyboardButton(text="🃏 Выбрать карты")],
        [KeyboardButton(text="⬅️ Вернуться назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True) 