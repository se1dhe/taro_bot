"""
Обработчик команды /help
"""
from aiogram import Router, types, F
from aiogram.filters import Command

router = Router()

HELP_TEXT = """
Добро пожаловать в бота-таролога! 🎴

Доступные команды:
/start - Начать работу с ботом
/help - Показать это сообщение

Как пользоваться ботом:
1. Нажмите /start для регистрации
2. Задайте свой вопрос боту
3. Получите предсказание на картах Таро

Тарифы:
- Малый (3 попытки) - 99 руб.
- Средний (10 попыток) - 199 руб.
- Безлимитный - 299 руб.

Пригласите друзей и получите бонусные попытки!
"""

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(HELP_TEXT)

@router.message(F.text == "ℹ️ Помощь")
async def help_button(message: types.Message):
    await message.answer(HELP_TEXT) 