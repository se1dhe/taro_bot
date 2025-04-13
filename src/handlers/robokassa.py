import hashlib
from datetime import datetime, timedelta
from aiohttp import web
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import ROBOKASSA_PASSWORD2
from database.models import Payment, User

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
    session: AsyncSession = request.app['db_session']
    
    # Находим платеж
    payment = await session.execute(
        select(Payment).where(Payment.payment_id == inv_id)
    )
    payment = payment.scalar_one_or_none()
    
    if not payment:
        return web.Response(text="payment not found")
    
    if payment.status == 'completed':
        return web.Response(text="payment already processed")
    
    # Обновляем статус платежа
    payment.status = 'completed'
    payment.completed_at = datetime.utcnow()
    
    # Находим пользователя
    user = await session.execute(
        select(User).where(User.telegram_id == payment.user_id)
    )
    user = user.scalar_one_or_none()
    
    if not user:
        return web.Response(text="user not found")
    
    # Обновляем данные пользователя
    if payment.readings_count == -1:  # безлимитный тариф
        user.is_unlimited = True
        user.unlimited_until = datetime.utcnow() + timedelta(days=payment.duration_days)
    else:
        user.readings_left += payment.readings_count
    
    # Сохраняем изменения
    await session.commit()
    
    return web.Response(text="OK") 