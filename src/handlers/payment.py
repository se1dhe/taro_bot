"""
Обработчик платежей
"""
import hashlib
from datetime import datetime, timedelta
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from config import (
    ROBOKASSA_LOGIN, ROBOKASSA_PASSWORD1,
    TARIFF_SMALL_PRICE, TARIFF_SMALL_READINGS, TARIFF_SMALL_DURATION,
    TARIFF_MEDIUM_PRICE, TARIFF_MEDIUM_READINGS, TARIFF_MEDIUM_DURATION,
    TARIFF_UNLIMITED_PRICE, TARIFF_UNLIMITED_DURATION
)
from keyboards.payment import get_payment_menu
from database.models import User, Payment

router = Router()

@router.message(F.text == "💫 Купить расклады")
async def handle_buy_subscription(message: Message, session: AsyncSession):
    """Обработчик кнопки покупки раскладов из главного меню"""
    # Проверяем, существует ли пользователь
    user = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    )
    user = user.scalar_one_or_none()
    
    if not user:
        await message.answer("Пожалуйста, сначала нажмите /start")
        return

    text = "👋 Расклады - виртуальная валюта, которой ты можешь оплачивать свои запросы к вселенной. Бесплатно получить их можно пригласив друзей, также можно купить их."
    await message.answer(text, reply_markup=get_payment_menu())

@router.message(Command("buy"))
async def show_payment_menu(message: Message):
    """Показывает меню оплаты"""
    text = "👋 Расклады - виртуальная валюта, которой ты можешь оплачивать свои запросы к вселенной. Бесплатно получить их можно пригласив друзей, также можно купить их."
    await message.answer(text, reply_markup=get_payment_menu())

@router.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: CallbackQuery):
    """Обрабатывает нажатие на кнопки покупки тарифов"""
    tariff = callback.data.split("_")[1]
    
    # Формируем данные для оплаты в зависимости от тарифа
    if tariff == "small":
        amount = TARIFF_SMALL_PRICE
        description = f"Тариф на {TARIFF_SMALL_READINGS} расклада"
        readings = TARIFF_SMALL_READINGS
        duration = TARIFF_SMALL_DURATION
    elif tariff == "medium":
        amount = TARIFF_MEDIUM_PRICE
        description = f"Тариф на {TARIFF_MEDIUM_READINGS} раскладов"
        readings = TARIFF_MEDIUM_READINGS
        duration = TARIFF_MEDIUM_DURATION
    else:  # unlimited
        amount = TARIFF_UNLIMITED_PRICE
        description = "Безлимитный тариф на месяц"
        readings = -1  # -1 означает безлимит
        duration = TARIFF_UNLIMITED_DURATION

    # Создаем уникальный идентификатор платежа
    payment_id = f"{callback.from_user.id}_{int(datetime.now().timestamp())}"
    
    # Создаем подпись для Robokassa
    signature = hashlib.md5(f"{ROBOKASSA_LOGIN}:{amount}:{payment_id}:{ROBOKASSA_PASSWORD1}".encode()).hexdigest()
    
    # Формируем ссылку для оплаты
    payment_url = f"https://auth.robokassa.ru/Merchant/Index.aspx?" \
                 f"MerchantLogin={ROBOKASSA_LOGIN}&" \
                 f"OutSum={amount}&" \
                 f"InvId={payment_id}&" \
                 f"Description={description}&" \
                 f"SignatureValue={signature}&" \
                 f"IsTest=1"  # Уберите в продакшене

    # Сохраняем информацию о платеже в базу данных
    payment = Payment(
        user_id=callback.from_user.id,
        amount=amount,
        payment_id=payment_id,
        readings_count=readings,
        duration_days=duration,
        status="pending",
        created_at=datetime.utcnow()
    )
    
    # Сохраняем платеж в базу данных
    session = callback.message.bot.session
    session.add(payment)
    await session.commit()
    
    await callback.message.answer(
        f"💫 Отлично! Вы выбрали тариф:\n"
        f"- {description}\n"
        f"- Стоимость: {amount}₽\n\n"
        f"Выберите способ оплаты:",
        reply_markup=get_payment_methods_keyboard(payment_url, payment_id)
    )
    await callback.answer()

@router.callback_query(F.data == "get_free_readings")
async def process_free_readings(callback: CallbackQuery):
    """Обрабатывает получение бесплатных раскладов"""
    await callback.message.answer(
        "🎁 Чтобы получить бесплатные расклады, пригласите друзей в бота!\n"
        "За каждого приглашенного друга вы получите 1 бесплатный расклад.\n\n"
        "Ваша реферальная ссылка: https://t.me/your_bot?start=ref_" + str(callback.from_user.id)
    )
    await callback.answer()

@router.callback_query(F.data == "pay_stars")
async def process_stars_payment(callback: CallbackQuery):
    """Обрабатывает оплату через Telegram Stars"""
    # Здесь будет код для создания платежа через Telegram Stars
    await callback.message.answer(
        "⭐️ Оплата через Telegram Stars временно недоступна.\n"
        "Пожалуйста, выберите другой способ оплаты."
    )
    await callback.answer()

def get_payment_methods_keyboard(payment_url: str, payment_id: str):
    """Создает клавиатуру с методами оплаты"""
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(
        text="💳 Оплатить картой",
        url=payment_url
    ))
    
    builder.row(InlineKeyboardButton(
        text="⭐️ Оплатить через Telegram Stars",
        callback_data=f"stars_{payment_id}"
    ))
    
    return builder.as_markup() 