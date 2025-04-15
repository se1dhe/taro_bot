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
from aiohttp import web

from config import BOT_TOKEN, DATABASE_URL, REDIS_URL
from handlers import start, question, payment, help, robokassa
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

# Настройка базы данных
engine = create_async_engine(
    f"postgresql+asyncpg://{DATABASE_URL.split('://', 1)[1]}",
    echo=True
)
async_session = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    """Инициализация базы данных"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def on_startup(app: web.Application):
    """Действия при запуске приложения"""
    await init_db()
    
    # Регистрация middleware для всех типов обновлений
    dp.message.middleware(DatabaseMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
    dp.update.middleware(DatabaseMiddleware())
    dp.edited_message.middleware(DatabaseMiddleware())
    dp.channel_post.middleware(DatabaseMiddleware())
    dp.edited_channel_post.middleware(DatabaseMiddleware())
    dp.inline_query.middleware(DatabaseMiddleware())
    dp.chosen_inline_result.middleware(DatabaseMiddleware())
    dp.pre_checkout_query.middleware(DatabaseMiddleware())
    dp.poll.middleware(DatabaseMiddleware())
    dp.poll_answer.middleware(DatabaseMiddleware())
    dp.my_chat_member.middleware(DatabaseMiddleware())
    dp.chat_member.middleware(DatabaseMiddleware())
    dp.chat_join_request.middleware(DatabaseMiddleware())
    
    # Регистрация роутеров в правильном порядке
    dp.include_router(help_router)  # Сначала регистрируем help, чтобы он не перехватывал другие команды
    dp.include_router(start_router)
    dp.include_router(payment_router)
    dp.include_router(tarot_router)
    dp.include_router(question_router)  # Question router должен быть последним, так как он обрабатывает общие сообщения
    
    # Запуск бота
    await dp.start_polling(bot)

async def create_app():
    """Создание веб-приложения"""
    app = web.Application()
    app['db_session'] = async_session
    
    # Добавляем маршруты
    app.router.add_post('/robokassa/result', robokassa.handle_robokassa_result)
    app.router.add_get('/robokassa/success', robokassa.handle_robokassa_success)
    app.router.add_get('/robokassa/fail', robokassa.handle_robokassa_fail)
    
    app.on_startup.append(on_startup)
    return app

if __name__ == "__main__":
    app = asyncio.run(create_app())
    web.run_app(app, host='0.0.0.0', port=8000) 