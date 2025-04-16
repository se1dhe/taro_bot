"""
Обработчики платежей
"""
import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import uuid
import hashlib
from urllib import parse
from urllib.parse import urlparse
import decimal
import json

from src.config import (
    TARIFF_SMALL_PRICE_RUB as TARIFF_SMALL_PRICE,
    TARIFF_SMALL_PRICE_STARS,
    TARIFF_SMALL_READINGS,
    TARIFF_SMALL_DURATION,
    TARIFF_MEDIUM_PRICE_RUB as TARIFF_MEDIUM_PRICE,
    TARIFF_MEDIUM_PRICE_STARS,
    TARIFF_MEDIUM_READINGS,
    TARIFF_MEDIUM_DURATION,
    TARIFF_UNLIMITED_PRICE_RUB as TARIFF_UNLIMITED_PRICE,
    TARIFF_UNLIMITED_PRICE_STARS,
    TARIFF_UNLIMITED_DURATION,
    ROBOKASSA_LOGIN,
    ROBOKASSA_PASSWORD1
)
from src.database.models import User, Payment
from src.database.database import get_user, update_user_readings

# Настройка логгера
logger = logging.getLogger(__name__)

router = Router()

class PaymentStates(StatesGroup):
    waiting_for_payment = State()

def calculate_signature(*args) -> str:
    """Create signature MD5."""
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()

def parse_response(request: str) -> dict:
    """
    :param request: Link.
    :return: Dictionary.
    """
    params = {}
    for item in urlparse(request).query.split('&'):
        key, value = item.split('=')
        params[key] = value
    return params

def check_signature_result(
    order_number: int,  # invoice number
    received_sum: decimal,  # cost of goods, RU
    received_signature: str,  # SignatureValue
    password: str  # Merchant password
) -> bool:
    signature = calculate_signature(received_sum, order_number, password)
    if signature.lower() == received_signature.lower():
        return True
    return False

def generate_payment_link(
    merchant_login: str,  # Merchant login
    merchant_password_1: str,  # Merchant password
    cost: decimal,  # Cost of goods, RU
    number: int,  # Invoice number
    description: str,  # Description of the purchase
    is_test = 0,
    robokassa_payment_url = 'https://auth.robokassa.ru/Merchant/Index.aspx',
) -> str:
    """URL for redirection of the customer to the service."""
    signature = calculate_signature(
        merchant_login,
        cost,
        number,
        merchant_password_1
    )

    data = {
        'MerchantLogin': merchant_login,
        'OutSum': cost,
        'InvId': number,
        'Description': description,
        'SignatureValue': signature,
    }
    
    if is_test != 0:
        data['IsTest'] = is_test
        
    return f'{robokassa_payment_url}?{parse.urlencode(data)}'

def result_payment(merchant_password_2: str, request: str) -> str:
    """Verification of notification (ResultURL).
    :param request: HTTP parameters.
    """
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']

    if check_signature_result(number, cost, signature, merchant_password_2):
        return f'OK{param_request["InvId"]}'
    return "bad sign"

def check_success_payment(merchant_password_1: str, request: str) -> str:
    """Verification of operation parameters ("cashier check") in SuccessURL script.
    :param request: HTTP parameters
    """
    param_request = parse_response(request)
    cost = param_request['OutSum']
    number = param_request['InvId']
    signature = param_request['SignatureValue']

    if check_signature_result(number, cost, signature, merchant_password_1):
        return "Thank you for using our service"
    return "bad sign"

@router.message(F.text == "💫 Купить расклады")
async def handle_buy_subscription(message: Message, session: AsyncSession):
    """Обработка команды покупки раскладов"""
    logger.info("====================================")
    logger.info("============ ВЕРСИЯ: 5  ============")
    logger.info("====================================")
    
    user = await get_user(message.from_user.id, session)
    logger.info(f"Пользователь {user.id} запросил покупку раскладов")
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔮 Малый (3 расклада)", callback_data="buy_small"),
                InlineKeyboardButton(text="✨ Средний (10 раскладов)", callback_data="buy_medium")
            ],
            [
                InlineKeyboardButton(text="🌟 Безлимитный", callback_data="buy_unlimited")
            ]
        ]
    )
    
    await message.answer(
        "Выберите тариф:\n\n"
        "🔮 Малый - 3 расклада\n"
        f"💰 {TARIFF_SMALL_PRICE}₽ или {TARIFF_SMALL_PRICE_STARS}⭐️\n\n"
        "✨ Средний - 10 раскладов\n"
        f"💰 {TARIFF_MEDIUM_PRICE}₽ или {TARIFF_MEDIUM_PRICE_STARS}⭐️\n\n"
        "🌟 Безлимитный\n"
        f"💰 {TARIFF_UNLIMITED_PRICE}₽ или {TARIFF_UNLIMITED_PRICE_STARS}⭐️",
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора тарифа"""
    tariff_type = callback.data.split("_")[1]
    
    # Определяем параметры тарифа
    tariff_params = {
        "small": {
            "price": TARIFF_SMALL_PRICE,
            "price_stars": TARIFF_SMALL_PRICE_STARS,
            "readings": TARIFF_SMALL_READINGS,
            "duration": TARIFF_SMALL_DURATION,
            "name": "Малый"
        },
        "medium": {
            "price": TARIFF_MEDIUM_PRICE,
            "price_stars": TARIFF_MEDIUM_PRICE_STARS,
            "readings": TARIFF_MEDIUM_READINGS,
            "duration": TARIFF_MEDIUM_DURATION,
            "name": "Средний"
        },
        "unlimited": {
            "price": TARIFF_UNLIMITED_PRICE,
            "price_stars": TARIFF_UNLIMITED_PRICE_STARS,
            "readings": -1,  # безлимитно
            "duration": TARIFF_UNLIMITED_DURATION,
            "name": "Безлимитный"
        }
    }
    
    if tariff_type not in tariff_params:
        await callback.answer("Неверный тариф", show_alert=True)
        return
    
    selected_tariff = tariff_params[tariff_type]
    payment_id = str(uuid.uuid4())
    
    # Сохраняем данные в состоянии
    await state.update_data(
        payment_id=payment_id,
        tariff=tariff_type,
        price_rub=selected_tariff["price"],
        price_stars=selected_tariff["price_stars"],
        readings=selected_tariff["readings"],
        duration=selected_tariff["duration"]
    )
    
    # Создаем клавиатуру с выбором способа оплаты
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"💳 Оплатить {selected_tariff['price']}₽",
                    callback_data=f"pay_robokassa_{payment_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"⭐️ Оплатить {selected_tariff['price_stars']} звезд",
                    callback_data=f"pay_stars_{payment_id}"
                )
            ],
            [
                InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_tariffs")
            ]
        ]
    )
    
    await callback.message.edit_text(
        f"Вы выбрали тариф '{selected_tariff['name']}'\n\n"
        f"Количество раскладов: {selected_tariff['readings'] if selected_tariff['readings'] != -1 else 'безлимитно'}\n"
        f"Срок действия: {selected_tariff['duration']} дней\n\n"
        "Выберите способ оплаты:",
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("pay_robokassa_"))
async def process_robokassa_payment(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обработка оплаты через Robokassa"""
    data = await state.get_data()
    payment_id = data.get("payment_id")
    price_rub = data.get("price_rub")
    readings = data.get("readings")
    
    try:
        # Создаем запись о платеже в базе данных
        user = await get_user(callback.from_user.id, session)
        new_payment = Payment(
            user_id=user.id,
            amount=int(price_rub),  # Преобразуем decimal в int
            currency="RUB",
            status="PENDING",
            payment_id=payment_id,
            readings_count=readings,
            duration_days=data.get("duration"),
            created_at=datetime.utcnow()
        )
        
        session.add(new_payment)
        await session.commit()
        
        # Генерируем числовой идентификатор для Robokassa из UUID
        numeric_inv_id = int(hashlib.md5(payment_id.encode()).hexdigest()[:7], 16) % 10000000
        logger.info(f"Преобразован UUID {payment_id} в числовой ID {numeric_inv_id}")
        
        # Генерируем ссылку на оплату через Robokassa
        payment_link = generate_payment_link(
            merchant_login=ROBOKASSA_LOGIN,
            merchant_password_1=ROBOKASSA_PASSWORD1,
            cost=price_rub,
            number=numeric_inv_id,
            description=f"Оплата тарифа {data.get('tariff')}",
            is_test=0
        )
        
        # Создаем клавиатуру с кнопкой для оплаты
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="💳 Оплатить",
                        url=payment_link
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔄 Проверить оплату",
                        callback_data=f"check_payment_{payment_id}"
                    )
                ],
                [
                    InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_tariffs")
                ]
            ]
        )
        
        await callback.message.edit_text(
            "Для оплаты нажмите на кнопку ниже. После оплаты нажмите 'Проверить оплату'.\n\n"
            f"Сумма к оплате: {price_rub}₽",
            reply_markup=keyboard
        )
        
    except Exception as e:
        logger.error(f"Ошибка при создании платежа: {e}")
        await callback.answer("Произошла ошибка при создании платежа. Пожалуйста, попробуйте позже.", show_alert=True)
        await state.clear()

@router.callback_query(F.data.startswith("pay_stars_"))
async def process_stars_payment(callback: CallbackQuery, state: FSMContext):
    """Обработка оплаты звездами"""
    data = await state.get_data()
    price_stars = data.get("price_stars")
    readings = data.get("readings")
    
    await callback.message.answer_invoice(
        title=f"Тариф '{data.get('tariff')}'",
        description=f"Покупка {readings if readings != -1 else 'безлимитного количества'} раскладов",
        payload=data.get("payment_id"),
        provider_token="",  # Для Stars оставляем пустым
        currency="XTR",
        prices=[LabeledPrice(label="XTR", amount=price_stars)],
        start_parameter=data.get("payment_id")
    )

@router.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    """Предварительная проверка платежа"""
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(message: Message, state: FSMContext, session: AsyncSession):
    """Обработка успешного платежа"""
    payment_data = await state.get_data()
    readings = payment_data.get("readings")
    
    # Получаем пользователя из базы данных
    user = await get_user(message.from_user.id, session)
    
    if user:
        # Если у пользователя уже есть расклады, добавляем новые
        current_readings = user.readings_left if user.readings_left != -1 else 0
        new_readings = -1 if readings == -1 or current_readings == -1 else current_readings + readings
        
        # Обновляем количество раскладов
        await update_user_readings(user.id, new_readings, session)
        
        await message.answer(
            f"🎉 Спасибо за оплату! Вам доступно "
            f"{'безлимитное количество' if new_readings == -1 else str(new_readings)} раскладов."
        )
    else:
        await message.answer("❌ Произошла ошибка при обновлении данных. Пожалуйста, обратитесь в поддержку.")
    
    await state.clear()

@router.callback_query(F.data.startswith("check_payment_"))
async def check_payment_status(callback: CallbackQuery, session: AsyncSession):
    """Проверка статуса платежа"""
    payment_id = callback.data.split("_")[2]
    
    # Находим платеж в базе данных
    payment = await session.execute(
        select(Payment).where(Payment.payment_id == payment_id)
    )
    payment = payment.scalar_one_or_none()
    
    if not payment:
        await callback.answer("Платеж не найден", show_alert=True)
        return
    
    if payment.status == "COMPLETED":
        # Платеж успешно выполнен
        user = await get_user(callback.from_user.id, session)
        
        # Обновляем информацию о количестве раскладов
        if payment.readings_count == -1:  # безлимитный тариф
            await update_user_readings(user.id, -1, session)
        else:
            # Используем правильный атрибут для получения текущего количества раскладов
            current_readings = user.readings_left if hasattr(user, 'readings_left') else 0
            if hasattr(user, 'readings_remaining') and not hasattr(user, 'readings_left'):
                current_readings = user.readings_remaining
                
            if current_readings == -1:
                new_readings = -1
            else:
                new_readings = current_readings + payment.readings_count
                
            await update_user_readings(user.id, new_readings, session)
        
        await callback.message.edit_text(
            "✅ Оплата успешно выполнена!\n\n"
            f"Вам доступно {'безлимитное количество' if payment.readings_count == -1 else str(payment.readings_count)} раскладов.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔮 Сделать расклад", callback_data="make_reading")]
                ]
            )
        )
    else:
        # Платеж еще не выполнен или отменен
        await callback.message.edit_text(
            "⏳ Ваш платеж еще обрабатывается или был отменен.\n\n"
            "Если вы уже произвели оплату, но видите это сообщение, пожалуйста, подождите немного. "
            "Обработка платежа может занять до 5 минут.\n\n"
            "Вы можете проверить статус платежа повторно или вернуться к выбору тарифов.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔄 Проверить снова", callback_data=f"check_payment_{payment_id}")],
                    [InlineKeyboardButton(text="⬅️ Назад к тарифам", callback_data="back_to_tariffs")]
                ]
            )
        )

@router.callback_query(F.data == "back_to_tariffs")
async def back_to_tariffs(callback: CallbackQuery, state: FSMContext):
    """Возврат к выбору тарифов"""
    await state.clear()
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔮 Малый (3 расклада)", callback_data="buy_small"),
                InlineKeyboardButton(text="✨ Средний (10 раскладов)", callback_data="buy_medium")
            ],
            [
                InlineKeyboardButton(text="🌟 Безлимитный", callback_data="buy_unlimited")
            ]
        ]
    )
    
    await callback.message.edit_text(
        "Выберите тариф:\n\n"
        "🔮 Малый - 3 расклада\n"
        f"💰 {TARIFF_SMALL_PRICE}₽ или {TARIFF_SMALL_PRICE_STARS}⭐️\n\n"
        "✨ Средний - 10 раскладов\n"
        f"💰 {TARIFF_MEDIUM_PRICE}₽ или {TARIFF_MEDIUM_PRICE_STARS}⭐️\n\n"
        "🌟 Безлимитный\n"
        f"💰 {TARIFF_UNLIMITED_PRICE}₽ или {TARIFF_UNLIMITED_PRICE_STARS}⭐️",
        reply_markup=keyboard
    )