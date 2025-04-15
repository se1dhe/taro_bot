"""
Обработчики уведомлений от Robokassa
"""
import hashlib
from datetime import datetime, timedelta
from aiohttp import web
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import ROBOKASSA_PASSWORD1, ROBOKASSA_PASSWORD2
from src.database.models import Payment, User
from src.database.database import update_user_readings

async def handle_robokassa_result(request: web.Request) -> web.Response:
    """Обрабатывает уведомления от Robokassa"""
    data = await request.post()
    
    # Получаем данные платежа
    out_sum = data.get('OutSum')
    inv_id = data.get('InvId')
    signature = data.get('SignatureValue')
    
    # Проверяем подпись
    expected_signature = hashlib.md5(f"{out_sum}:{inv_id}:{ROBOKASSA_PASSWORD2}".encode()).hexdigest()
    
    if signature.lower() != expected_signature.lower():
        return web.Response(text="bad signature")
    
    # Получаем сессию базы данных
    session = request.app['db_session']
    
    # Находим платеж
    payment = await session.execute(
        select(Payment).where(Payment.payment_id == inv_id)
    )
    payment = payment.scalar_one_or_none()
    
    if not payment:
        return web.Response(text="payment not found")
    
    if payment.status == 'COMPLETED':
        return web.Response(text="payment already processed")
    
    # Обновляем статус платежа
    payment.status = 'COMPLETED'
    payment.completed_at = datetime.utcnow()
    
    # Находим пользователя
    user = await session.execute(
        select(User).where(User.id == payment.user_id)
    )
    user = user.scalar_one_or_none()
    
    if not user:
        return web.Response(text="user not found")
    
    # Обновляем данные пользователя
    if payment.readings_count == -1:  # безлимитный тариф
        user.readings_remaining = -1
        user.subscription_end = datetime.utcnow() + timedelta(days=payment.duration_days)
    else:
        # Если у пользователя уже есть расклады, добавляем новые
        current_readings = user.readings_remaining if user.readings_remaining != -1 else 0
        new_readings = -1 if payment.readings_count == -1 or current_readings == -1 else current_readings + payment.readings_count
        user.readings_remaining = new_readings
    
    # Сохраняем изменения
    await session.commit()
    
    return web.Response(text="OK")

async def handle_robokassa_success(request: web.Request) -> web.Response:
    """Обрабатывает перенаправление при успешной оплате"""
    data = request.query
    
    # Получаем данные платежа
    out_sum = data.get('OutSum')
    inv_id = data.get('InvId')
    signature = data.get('SignatureValue')
    
    # Проверяем подпись
    expected_signature = hashlib.md5(f"{out_sum}:{inv_id}:{ROBOKASSA_PASSWORD1}".encode()).hexdigest()
    
    if signature.lower() != expected_signature.lower():
        return web.Response(text="<html><body><h1>Неверная подпись</h1><p>Вернитесь в бот</p></body></html>", 
                           content_type="text/html")
    
    # Отображаем страницу с успешной оплатой
    return web.Response(text="""
    <html>
    <head>
        <title>Успешная оплата</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
                background-color: #f0f2f5;
            }
            .success-container {
                max-width: 500px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #4CAF50;
            }
            .back-button {
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
                font-weight: bold;
            }
            .icon {
                font-size: 50px;
                color: #4CAF50;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="success-container">
            <div class="icon">✅</div>
            <h1>Оплата успешно выполнена!</h1>
            <p>Ваш платеж был успешно обработан. Вернитесь в бот, чтобы продолжить работу.</p>
            <a href="https://t.me/sedhe_dev" class="back-button">Вернуться в бот</a>
        </div>
    </body>
    </html>
    """, content_type="text/html")

async def handle_robokassa_fail(request: web.Request) -> web.Response:
    """Обрабатывает перенаправление при неудачной оплате"""
    # Отображаем страницу с неудачной оплатой
    return web.Response(text="""
    <html>
    <head>
        <title>Оплата не выполнена</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 20px;
                background-color: #f0f2f5;
            }
            .fail-container {
                max-width: 500px;
                margin: 0 auto;
                background-color: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #F44336;
            }
            .back-button {
                display: inline-block;
                background-color: #2196F3;
                color: white;
                padding: 12px 24px;
                text-decoration: none;
                border-radius: 5px;
                margin-top: 20px;
                font-weight: bold;
            }
            .icon {
                font-size: 50px;
                color: #F44336;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="fail-container">
            <div class="icon">❌</div>
            <h1>Оплата не выполнена</h1>
            <p>К сожалению, ваш платеж не был завершен. Вернитесь в бот, чтобы повторить попытку.</p>
            <a href="https://t.me/sedhe_dev" class="back-button">Вернуться в бот</a>
        </div>
    </body>
    </html>
    """, content_type="text/html") 