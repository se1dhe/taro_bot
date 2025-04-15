"""
Обработчики платежей
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, LabeledPrice, PreCheckoutQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import urllib.parse
from datetime import datetime
from src.config import (
    TARIFF_SMALL_PRICE_STARS, TARIFF_SMALL_READINGS,
    TARIFF_MEDIUM_PRICE_STARS, TARIFF_MEDIUM_READINGS,
    TARIFF_UNLIMITED_PRICE_STARS,
    TARIFF_SMALL_PRICE_RUB, TARIFF_MEDIUM_PRICE_RUB, TARIFF_UNLIMITED_PRICE_RUB,
    ROBOKASSA_LOGIN, ROBOKASSA_PASSWORD1, ROBOKASSA_TEST_MODE,
    ROBOKASSA_SUCCESS_URL, ROBOKASSA_FAIL_URL,
    TAROT_SETTINGS, BOT_USERNAME
)
from src.keyboards.payment import get_payment_menu, get_payment_methods_keyboard
from src.database.database import get_user, update_user_readings
from src.database.models import User, Payment
import uuid
from hashlib import md5
import json
import base64

router = Router()

class PaymentStates(StatesGroup):
    waiting_for_payment = State()

@router.message(F.text == "💫 Купить расклады")
async def handle_buy_subscription(message: Message, session: AsyncSession):
    """Обработка команды покупки раскладов"""
    # Получаем информацию о пользователе
    user = await get_user(message.from_user.id, session)
    
    await message.answer(
        "Выберите тариф:",
        reply_markup=get_payment_menu(user)
    )

@router.callback_query(F.data == "get_free_readings")
async def handle_get_free_readings(callback: CallbackQuery, session: AsyncSession):
    """Обработка нажатия на кнопку 'Получить расклады бесплатно'"""
    # Получаем информацию о пользователе
    user = await get_user(callback.from_user.id, session)
    
    # Получаем сумму платежей от рефералов
    total_referral_payments = 0
    if user.referrals_count > 0:
        referrals = await session.execute(
            select(User).where(User.referral_id == user.id)
        )
        referrals = referrals.scalars().all()
        
        for referral in referrals:
            payments = await session.execute(
                select(Payment).where(Payment.user_id == referral.id)
            )
            payments = payments.scalars().all()
            total_referral_payments += sum(payment.amount for payment in payments)
    
    # Формируем реферальную ссылку
    referral_link = f"https://t.me/{BOT_USERNAME}?start=ref_{user.id}"
    
    # Создаем клавиатуру с кнопкой "Назад"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️ Назад",
                    callback_data="back_to_tariffs"
                )
            ]
        ]
    )
    
    # Показываем информацию о реферальной системе
    await callback.message.edit_text(
        "🎁 Получите бесплатные расклады, приглашая друзей!\n\n"
        f"👥 Приглашено пользователей: {user.referrals_count}\n"
        f"💰 Сумма платежей от рефералов: {total_referral_payments} ⭐️\n\n"
        f"🔗 Ваша реферальная ссылка:\n{referral_link}",
        reply_markup=keyboard
    )

@router.callback_query(F.data == "back_to_tariffs")
async def handle_back_to_tariffs(callback: CallbackQuery, session: AsyncSession):
    """Обработка нажатия на кнопку 'Назад'"""
    # Получаем информацию о пользователе
    user = await get_user(callback.from_user.id, session)
    
    await callback.message.edit_text(
        "Выберите тариф:",
        reply_markup=get_payment_menu(user)
    )

@router.callback_query(F.data == "show_referrals")
async def handle_show_referrals(callback: CallbackQuery, session: AsyncSession):
    """Обработка нажатия на кнопку 'Показать рефералов'"""
    # Получаем информацию о пользователе
    user = await get_user(callback.from_user.id, session)
    
    # Показываем информацию о рефералах
    await callback.message.edit_text(
        f"👥 Ваши рефералы:\n\n"
        f"Приглашено пользователей: {user.referrals_count}\n"
        f"Получено бонусных раскладов: {user.referrals_count * TAROT_SETTINGS['referral_bonus_readings']}\n\n"
        "Продолжайте приглашать друзей, чтобы получать больше бонусов!",
        reply_markup=get_referral_info_keyboard(user)
    )

@router.callback_query(F.data == "show_bonuses")
async def handle_show_bonuses(callback: CallbackQuery, session: AsyncSession):
    """Обработка нажатия на кнопку 'Показать бонусы'"""
    # Получаем информацию о пользователе
    user = await get_user(callback.from_user.id, session)
    
    # Показываем информацию о бонусах
    await callback.message.edit_text(
        "🎁 Бонусная система:\n\n"
        f"За каждого приглашенного друга вы получаете {TAROT_SETTINGS['referral_bonus_readings']} раскладов.\n"
        f"У вас уже приглашено {user.referrals_count} пользователей.\n"
        f"Всего получено бонусных раскладов: {user.referrals_count * TAROT_SETTINGS['referral_bonus_readings']}\n\n"
        "Приглашайте друзей и получайте больше бонусов!",
        reply_markup=get_referral_info_keyboard(user)
    )

@router.callback_query(F.data.startswith("buy_"))
async def process_buy(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора тарифа"""
    tariff = callback.data.split("_")[1]
    payment_id = str(uuid.uuid4())
    
    # Определяем цену и количество раскладов в зависимости от тарифа
    if tariff == "small":
        price_rub = TARIFF_SMALL_PRICE_RUB
        price_stars = TARIFF_SMALL_PRICE_STARS
        readings = TARIFF_SMALL_READINGS
        title = "Тариф 'Малый'"
    elif tariff == "medium":
        price_rub = TARIFF_MEDIUM_PRICE_RUB
        price_stars = TARIFF_MEDIUM_PRICE_STARS
        readings = TARIFF_MEDIUM_READINGS
        title = "Тариф 'Средний'"
    else:
        price_rub = TARIFF_UNLIMITED_PRICE_RUB
        price_stars = TARIFF_UNLIMITED_PRICE_STARS
        readings = -1  # Безлимитный
        title = "Тариф 'Безлимитный'"
    
    await state.set_state(PaymentStates.waiting_for_payment)
    await state.update_data(
        tariff=tariff, 
        payment_id=payment_id, 
        price_rub=price_rub,
        price_stars=price_stars,
        readings=readings
    )
    
    # Формируем URL для оплаты через Robokassa
    merchant_login = ROBOKASSA_LOGIN
    password1 = ROBOKASSA_PASSWORD1
    
    # Формируем фискальные данные
    receipt = {
        "sno": "usn_income",
        "items": [
            {
                "name": title,
                "quantity": 1,
                "sum": price_rub,
                "payment_method": "full_payment",
                "payment_object": "service",
                "tax": "none"
            }
        ]
    }
    
    # Кодируем receipt в JSON и затем в URL-safe формат
    receipt_json = json.dumps(receipt, ensure_ascii=False)
    receipt_encoded = urllib.parse.quote(receipt_json)
    
    # Формируем строку для подписи
    signature_params = [
        merchant_login,      # MerchantLogin
        str(price_rub),     # OutSum
        payment_id,         # InvId
        receipt_encoded,    # Receipt
        password1           # Password1
    ]
    
    # Добавляем Shp_ параметры, если они есть
    user_id = callback.from_user.id
    signature_params.append(f"Shp_user_id={user_id}")
    
    # Формируем подпись
    signature_string = ":".join(signature_params)
    signature_hash = md5(signature_string.encode()).hexdigest().upper()
    
    # Формируем параметры для URL
    params = {
        "MerchantLogin": merchant_login,
        "OutSum": price_rub,
        "InvId": payment_id,
        "Description": f"Оплата тарифа {title}",
        "SignatureValue": signature_hash,
        "Receipt": receipt_encoded,
        "IsTest": 1 if ROBOKASSA_TEST_MODE else 0,
        "Culture": "ru",
        "Encoding": "utf-8",
        "Shp_user_id": user_id
    }
    
    # Формируем URL для оплаты
    robokassa_url = "https://auth.robokassa.ru/Merchant/Index.aspx?" + urllib.parse.urlencode(params)
    
    await callback.message.edit_text(
        f"Тариф '{title}'\n"
        f"Количество раскладов: {readings if readings != -1 else 'безлимитно'}\n"
        f"Стоимость: {price_rub}₽ / {price_stars}⭐️\n\n"
        "Выберите способ оплаты:",
        reply_markup=get_payment_methods_keyboard(payment_id, tariff, robokassa_url)
    )

@router.callback_query(F.data.startswith("pay_stars_"))
async def process_stars_payment(callback: CallbackQuery, state: FSMContext):
    """Обработка оплаты звездами"""
    data = await state.get_data()
    price_stars = data.get("price_stars")
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

@router.message(Command("paysupport"))
async def handle_pay_support(message: Message):
    """Обработка команды поддержки по платежам"""
    await message.answer(
        "По вопросам оплаты и возврата средств обращайтесь в поддержку: @support"
    )

@router.callback_query(F.data.startswith("pay_robokassa_"))
async def process_robokassa_payment(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Обработка оплаты через Robokassa"""
    data = await state.get_data()
    payment_id = data.get("payment_id")
    price_rub = data.get("price_rub")
    tariff = data.get("tariff")
    readings = data.get("readings")
    title = {
        "small": "Тариф 'Малый'",
        "medium": "Тариф 'Средний'",
        "unlimited": "Тариф 'Безлимитный'"
    }[tariff]
    
    # Создаем запись о платеже в базе данных
    user = await get_user(callback.from_user.id, session)
    
    # Создаем новую запись в таблице payments
    new_payment = Payment(
        user_id=user.id,
        amount=price_rub,
        currency="RUB",
        status="PENDING",
        payment_id=payment_id,
        readings_count=readings,
        duration_days=30,  # По умолчанию все тарифы на 30 дней
        created_at=datetime.utcnow()
    )
    
    session.add(new_payment)
    await session.commit()
    
    # Формируем URL для оплаты через Robokassa
    merchant_login = ROBOKASSA_LOGIN
    password1 = ROBOKASSA_PASSWORD1
    
    # Формируем фискальные данные
    receipt = {
        "sno": "usn_income",
        "items": [
            {
                "name": title,
                "quantity": 1,
                "sum": price_rub,
                "payment_method": "full_payment",
                "payment_object": "service",
                "tax": "none"
            }
        ]
    }
    
    # Кодируем receipt в JSON и затем в URL-safe формат
    receipt_json = json.dumps(receipt, ensure_ascii=False)
    receipt_encoded = urllib.parse.quote(receipt_json)
    
    # Формируем строку для подписи
    signature_params = [
        merchant_login,      # MerchantLogin
        str(price_rub),     # OutSum
        payment_id,         # InvId
        receipt_encoded,    # Receipt
        password1           # Password1
    ]
    
    # Добавляем Shp_ параметры, если они есть
    user_id = callback.from_user.id
    signature_params.append(f"Shp_user_id={user_id}")
    
    # Формируем подпись
    signature_string = ":".join(signature_params)
    signature_hash = md5(signature_string.encode()).hexdigest().upper()
    
    # Формируем параметры для URL
    params = {
        "MerchantLogin": merchant_login,
        "OutSum": price_rub,
        "InvId": payment_id,
        "Description": f"Оплата тарифа {title}",
        "SignatureValue": signature_hash,
        "Receipt": receipt_encoded,
        "IsTest": 1 if ROBOKASSA_TEST_MODE else 0,
        "Culture": "ru",
        "Encoding": "utf-8",
        "Shp_user_id": user_id,
        "SuccessURL": ROBOKASSA_SUCCESS_URL,
        "FailURL": ROBOKASSA_FAIL_URL
    }
    
    # Формируем URL для оплаты
    robokassa_url = "https://auth.robokassa.ru/Merchant/Index.aspx?" + urllib.parse.urlencode(params)
    
    # Отправляем пользователю ссылку на оплату
    await callback.message.edit_text(
        f"Оплата тарифа '{title}'\n"
        f"Количество раскладов: {readings if readings != -1 else 'безлимитно'}\n"
        f"Стоимость: {price_rub}₽\n\n"
        "Перейдите по ссылке ниже для оплаты:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="💳 Оплатить", url=robokassa_url)],
                [InlineKeyboardButton(text="🔄 Проверить оплату", callback_data=f"check_payment_{payment_id}")],
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_tariffs")]
            ]
        )
    )

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
            current_readings = user.readings_remaining if user.readings_remaining != -1 else 0
            new_readings = -1 if payment.readings_count == -1 or current_readings == -1 else current_readings + payment.readings_count
            await update_user_readings(user.id, new_readings, session)
        
        await callback.message.edit_text(
            "✅ Оплата успешно выполнена!\n\n"
            f"Вам доступно {'безлимитное количество' if payment.readings_count == -1 else payment.readings_count} раскладов.",
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