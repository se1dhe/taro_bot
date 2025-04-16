from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from src.config import BOT_TOKEN
from src.handlers.monthly_reading import router as monthly_reading_router
from src.handlers.payments import router as payments_router
from src.handlers.questions import router as questions_router
from src.keyboards.reply import get_main_keyboard

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация роутеров
dp.include_router(monthly_reading_router)
dp.include_router(payments_router)
dp.include_router(questions_router)

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Добро пожаловать в бота для гадания на картах Таро!",
        reply_markup=get_main_keyboard()
    )

async def main():
    await dp.start_polling(bot) 