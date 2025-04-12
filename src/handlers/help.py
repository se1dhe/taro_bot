"""
Обработчик команды /help
"""
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = """
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
    await message.answer(help_text) 