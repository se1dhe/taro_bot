"""
Обработчики платежей
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.config import (
    TARIFF_SMALL_PRICE_STARS, TARIFF_SMALL_READINGS,
    TARIFF_MEDIUM_PRICE_STARS, TARIFF_MEDIUM_READINGS,
    TARIFF_UNLIMITED_PRICE_STARS,
    ROBOKASSA_LOGIN, ROBOKASSA_PASSWORD1, ROBOKASSA_TEST_MODE
)
from src.keyboards.payment import get_payment_menu, get_payment_methods_keyboard
from src.database.database import get_user, update_user_readings
import uuid
from urllib.parse import urlencode
from hashlib import md5

router = Router()

class PaymentStates(StatesGroup):
    waiting_for_payment = State()

@router.message(F.text == "💫 Купить расклады")
async def handle_buy_subscription(message: Message):
    """Обработка команды покупки раскладов"""
    await message.answer(
        "Выберите тариф:",
        reply_markup=get_payment_menu()
    )

@router.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора тарифа"""
    tariff = callback.data.split("_")[1]
    payment_id = str(uuid.uuid4())
    
    # Определяем цену и количество раскладов в зависимости от тарифа
    if tariff == "small":
        price = TARIFF_SMALL_PRICE_STARS
        readings = TARIFF_SMALL_READINGS
        title = "Тариф 'Малый'"
    elif tariff == "medium":
        price = TARIFF_MEDIUM_PRICE_STARS
        readings = TARIFF_MEDIUM_READINGS
        title = "Тариф 'Средний'"
    else:
        price = TARIFF_UNLIMITED_PRICE_STARS
        readings = -1  # Безлимитный
        title = "Тариф 'Безлимитный'"
    
    await state.set_state(PaymentStates.waiting_for_payment)
    await state.update_data(tariff=tariff, payment_id=payment_id, price=price, readings=readings)
    
    # Формируем URL для оплаты через Robokassa
    merchant_login = ROBOKASSA_LOGIN
    password1 = ROBOKASSA_PASSWORD1
    
    signature = f"{merchant_login}:{price}:{payment_id}:{password1}"
    signature_hash = md5(signature.encode()).hexdigest()
    
    params = {
        "MerchantLogin": merchant_login,
        "OutSum": price,
        "InvId": payment_id,
        "Description": f"Оплата тарифа {title}",
        "SignatureValue": signature_hash,
        "IsTest": 1 if ROBOKASSA_TEST_MODE else 0
    }
    
    robokassa_url = f"https://auth.robokassa.ru/Merchant/Index.aspx?{urlencode(params)}"
    
    await callback.message.edit_text(
        f"Тариф '{title}'\n"
        f"Количество раскладов: {readings if readings != -1 else 'безлимитно'}\n"
        f"Стоимость: {price} ⭐️\n\n"
        "Выберите способ оплаты:",
        reply_markup=get_payment_methods_keyboard(payment_id, tariff, robokassa_url)
    )

@router.callback_query(F.data.startswith("pay_stars_"))
async def process_stars_payment(callback: CallbackQuery, state: FSMContext):
    """Обработка оплаты звездами"""
    data = await state.get_data()
    price = data.get("price")
    readings = data.get("readings")
    title = {
        "small": "Тариф 'Малый'",
        "medium": "Тариф 'Средний'",
        "unlimited": "Тариф 'Безлимитный'"
    }[data.get("tariff")]
    
    await callback.message.answer_invoice(
        title=title,
        description=f"Покупка {readings if readings != -1 else 'безлимитного количества'} раскладов",
        payload=data.get("payment_id"),
        provider_token="",  # Для Stars оставляем пустым
        currency="XTR",
        prices=[LabeledPrice(label="XTR", amount=price)],
        start_parameter=data.get("payment_id")
    )

@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    """Предварительная проверка платежа"""
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message, state: FSMContext):
    """Обработка успешного платежа"""
    payment_data = await state.get_data()
    readings = payment_data.get("readings")
    
    # Получаем пользователя из базы данных
    user = await get_user(message.from_user.id, message.bot.get("db"))
    
    if user:
        # Если у пользователя уже есть расклады, добавляем новые
        current_readings = user.readings_left if user.readings_left != -1 else 0
        new_readings = -1 if readings == -1 or current_readings == -1 else current_readings + readings
        
        # Обновляем количество раскладов
        await update_user_readings(user.id, new_readings, message.bot.get("db"))
        
        await message.answer(
            f"🎉 Спасибо за оплату! Вам доступно "
            f"{'безлимитное количество' if new_readings == -1 else str(new_readings)} раскладов."
        )
    else:
        await message.answer("❌ Произошла ошибка при обновлении данных. Пожалуйста, обратитесь в поддержку.")
    
    await state.clear()

@router.message(Command("paysupport"))
async def handle_pay_support(message: Message):
    """Обработка команды поддержки по платежам"""
    await message.answer(
        "По вопросам оплаты и возврата средств обращайтесь в поддержку: @support"
    ) 