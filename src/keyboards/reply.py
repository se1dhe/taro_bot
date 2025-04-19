"""
Клавиатуры для бота
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from src.config import WEBAPP_URL
import urllib.parse
from datetime import datetime

def get_monthly_reading_month() -> str:
    """
    Определяет месяц для расклада на основе текущей даты.
    Если текущая дата с 16 числа месяца по 15 число следующего месяца,
    то возвращает следующий месяц.
    """
    now = datetime.now()
    current_day = now.day
    
    if current_day >= 16:
        # Если текущий день >= 16, то следующий месяц
        next_month = now.month + 1
        if next_month > 12:
            next_month = 1
        month_names = {
            1: "январь", 2: "февраль", 3: "март", 4: "апрель",
            5: "май", 6: "июнь", 7: "июль", 8: "август",
            9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"
        }
        return month_names[next_month]
    else:
        # Если текущий день < 16, то текущий месяц
        month_names = {
            1: "январь", 2: "февраль", 3: "март", 4: "апрель",
            5: "май", 6: "июнь", 7: "июль", 8: "август",
            9: "сентябрь", 10: "октябрь", 11: "ноябрь", 12: "декабрь"
        }
        return month_names[now.month]

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Создает основную клавиатуру с главными действиями
    """
    month = get_monthly_reading_month()
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎴 Задать вопрос")],
            [KeyboardButton(
                text=f"📅 Расклад на {month}",
                web_app=WebAppInfo(url=f"{WEBAPP_URL}/monthly_reading")
            )],
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