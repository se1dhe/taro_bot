"""
Клавиатуры для бота
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from config import WEBAPP_URL
import urllib.parse

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает основную клавиатуру с главными действиями
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎴 Задать вопрос")],
            [KeyboardButton(text="💫 Купить расклады")],
            [KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )
    return keyboard

def get_question_actions_keyboard(question: str) -> ReplyKeyboardMarkup:
    """
    Создает клавиатуру для действий после ввода вопроса
    """
    encoded_question = urllib.parse.quote(question)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text="🃏 Выбрать карты",
                web_app=WebAppInfo(url=f"{WEBAPP_URL}?question={encoded_question}")
            )],
            [KeyboardButton(text="⬅️ Вернуться назад")]
        ],
        resize_keyboard=True
    )
    return keyboard 