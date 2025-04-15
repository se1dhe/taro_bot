"""
Обработчики платежей через Robokassa
"""
import logging
from aiogram import Router
from aiogram.types import Message
from aiohttp import web
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import hashlib
from src.config import ROBOKASSA_PASSWORD2
from src.database.models import Payment

# Настройка логгера
logger = logging.getLogger(__name__)

router = Router()

async def handle_robokassa_result(request: web.Request) -> web.Response:
    """Обработка результата платежа от Robokassa"""
    try:
        data = await request.post()
        logger.info(f"Получен результат платежа: {data}")
        
        # Проверяем подпись
        signature = f"{data['OutSum']}:{data['InvId']}:{ROBOKASSA_PASSWORD2}"
        if data.get('shp_user_id'):
            signature += f":shp_user_id={data['shp_user_id']}"
        
        calculated_signature = hashlib.md5(signature.encode('utf-8')).hexdigest()
        
        if calculated_signature.lower() != data['SignatureValue'].lower():
            logger.error(f"Неверная подпись платежа: {data}")
            return web.Response(text="ERROR: Invalid signature")
        
        # Получаем сессию из приложения
        session_maker = request.app['db_session']
        async with session_maker() as session:
            # Находим платеж в базе данных по InvId
            payment = await session.execute(
                select(Payment).where(Payment.payment_id == data['InvId'])
            )
            payment = payment.scalar_one_or_none()
            
            if not payment:
                # Ищем платеж по числовому ID (в случае если UUID был преобразован)
                logger.info(f"Платеж не найден по ID {data['InvId']}, ищем по другим критериям")
                
                # Получаем все ожидающие платежи
                all_payments = await session.execute(
                    select(Payment).where(Payment.status == "PENDING")
                )
                all_payments = all_payments.scalars().all()
                
                # Проверяем платежи на соответствие
                for p in all_payments:
                    # Проверяем числовое представление UUID
                    payment_numeric = ''.join(filter(str.isdigit, p.payment_id))
                    if data['InvId'] in payment_numeric:
                        payment = p
                        logger.info(f"Найден платеж по числовому представлению UUID: {p.payment_id}")
                        break
                
                # Ищем по сумме и пользователю, если по ID не нашли
                if not payment and data.get('shp_user_id'):
                    matching_payments = await session.execute(
                        select(Payment).where(
                            Payment.user_id == int(data['shp_user_id']),
                            Payment.amount == float(data['OutSum']),
                            Payment.status == "PENDING"
                        )
                    )
                    payment = matching_payments.scalar_one_or_none()
                    if payment:
                        logger.info(f"Найден платеж по пользователю {data['shp_user_id']} и сумме {data['OutSum']}")
            
            if payment:
                # Обновляем статус платежа
                payment.status = "COMPLETED"
                payment.completed_at = datetime.utcnow()
                await session.commit()
                logger.info(f"Платеж успешно обработан: {data['InvId']}")
                return web.Response(text=f"OK{data['InvId']}")
            else:
                logger.error(f"Платеж не найден: {data['InvId']}")
                return web.Response(text="ERROR: Payment not found")
    except Exception as e:
        logger.error(f"Ошибка при обработке платежа: {e}")
        return web.Response(text="ERROR: Internal server error")

async def handle_robokassa_success(request: web.Request) -> web.Response:
    """Обработка успешного платежа"""
    try:
        params = request.query
        logger.info(f"Получен запрос на страницу успешной оплаты: {params}")
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Оплата успешно выполнена</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 20px;
                    background-color: #f0f0f0;
                }
                .success-container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                .success-icon {
                    color: #2ecc71;
                    font-size: 64px;
                    margin-bottom: 20px;
                }
                h1 {
                    color: #333;
                    margin-bottom: 20px;
                }
                p {
                    color: #666;
                    margin-bottom: 30px;
                    line-height: 1.5;
                }
                .btn {
                    display: inline-block;
                    background-color: #3498db;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    transition: background-color 0.3s;
                }
                .btn:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>
        <body>
            <div class="success-container">
                <div class="success-icon">✅</div>
                <h1>Платеж успешно выполнен!</h1>
                <p>Спасибо за оплату. Ваш заказ успешно оформлен.</p>
                <p>Пожалуйста, вернитесь в Telegram и нажмите кнопку "Проверить оплату" для активации вашего тарифа.</p>
                <a href="https://t.me/se1dhe_bot" class="btn">Вернуться в бот</a>
            </div>
        </body>
        </html>
        """
        
        return web.Response(text=html, content_type='text/html')
    except Exception as e:
        logger.error(f"Ошибка при обработке успешного платежа: {e}")
        return web.Response(text="Платеж успешно выполнен! Вернитесь в бот и нажмите 'Проверить оплату'.")

async def handle_robokassa_fail(request: web.Request) -> web.Response:
    """Обработка неудачного платежа"""
    try:
        params = request.query
        logger.info(f"Получен запрос на страницу неудачной оплаты: {params}")
        
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Платеж не выполнен</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 20px;
                    background-color: #f0f0f0;
                }
                .fail-container {
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }
                .fail-icon {
                    color: #e74c3c;
                    font-size: 64px;
                    margin-bottom: 20px;
                }
                h1 {
                    color: #333;
                    margin-bottom: 20px;
                }
                p {
                    color: #666;
                    margin-bottom: 30px;
                    line-height: 1.5;
                }
                .btn {
                    display: inline-block;
                    background-color: #3498db;
                    color: white;
                    padding: 12px 24px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    transition: background-color 0.3s;
                }.btn:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>
        <body>
            <div class="fail-container">
                <div class="fail-icon">❌</div>
                <h1>Платеж не выполнен</h1>
                <p>К сожалению, во время оплаты произошла ошибка. Ваш платеж не был выполнен.</p>
                <p>Пожалуйста, вернитесь в Telegram и попробуйте снова, или выберите другой способ оплаты.</p>
                <a href="https://t.me/se1dhe_bot" class="btn">Вернуться в бот</a>
            </div>
        </body>
        </html>
        """
        
        return web.Response(text=html, content_type='text/html')
    except Exception as e:
        logger.error(f"Ошибка при обработке неудачного платежа: {e}")
        return web.Response(text="Платеж не выполнен. Пожалуйста, вернитесь в бот и попробуйте снова.")