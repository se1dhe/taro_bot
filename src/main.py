"""
Основной файл бота
"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject

from config import BOT_TOKEN, DATABASE_URL, REDIS_URL
from handlers import start, question, payment, help
from database.models import Base
from src.handlers.start import router as start_router
from src.handlers.tarot import router as tarot_router
from src.handlers.question import router as question_router
from src.handlers.payment import router as payment_router
from src.handlers.help import router as help_router

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = RedisStorage.from_url(REDIS_URL)
dp = Dispatcher(storage=storage)

# Настройка базы данных
engine = create_async_engine(
    f"postgresql+asyncpg://{DATABASE_URL.split('://', 1)[1]}",
    echo=True
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with async_session() as session:
            data["session"] = session
            return await handler(event, data)

async def init_db():
    """Инициализация базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    """Основная функция"""
    # Инициализация базы данных
    await init_db()
    
    # Добавляем middleware
    dp.update.middleware(DatabaseMiddleware())
    
    # Регистрация роутеров
    dp.include_router(start_router)
    dp.include_router(tarot_router)
    dp.include_router(question_router)
    dp.include_router(payment_router)
    dp.include_router(help_router)
    
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main()) 