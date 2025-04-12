"""
Обработчики для работы с вопросами
"""
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import json
import urllib.parse
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.filters import StateFilter

from keyboards.reply import get_main_keyboard, get_question_actions_keyboard
from database.models import User, Reading
from config import TAROT_SETTINGS, WEBAPP_URL
from utils.tarot import get_random_tarot_cards
from utils.openai import get_interpretation_from_openai

router = Router()

class QuestionStates(StatesGroup):
    """Состояния для работы с вопросами"""
    main_menu = State()            # Главное меню
    waiting_for_question = State() # Ожидание вопроса от пользователя
    waiting_for_cards = State()    # Ожидание выбора карт
    processing_reading = State()   # Обработка гадания
    choosing_cards = State()        # Выбор карт

@router.message(F.text == "🎴 Задать вопрос")
async def ask_question(message: types.Message, state: FSMContext):
    """
    Обработчик кнопки "Задать вопрос"
    """
    await state.set_state(QuestionStates.main_menu)
    await message.answer(
        "Пожалуйста, введите ваш вопрос. "
        "Постарайтесь сформулировать его максимально четко и конкретно."
    )
    await state.set_state(QuestionStates.waiting_for_question)

@router.message(QuestionStates.waiting_for_question)
async def process_question(message: types.Message, state: FSMContext, session: AsyncSession):
    """
    Обработчик ввода вопроса
    """
    # Проверяем, есть ли текст в сообщении
    if not message.text:
        await message.answer("Пожалуйста, введите текстовый вопрос.")
        return
    
    # Проверяем длину вопроса
    if len(message.text) < TAROT_SETTINGS["min_question_length"]:
        await message.answer(
            f"Вопрос слишком короткий. Минимальная длина: {TAROT_SETTINGS['min_question_length']} символов."
        )
        return
    
    if len(message.text) > TAROT_SETTINGS["max_question_length"]:
        await message.answer(
            f"Вопрос слишком длинный. Максимальная длина: {TAROT_SETTINGS['max_question_length']} символов."
        )
        return
    
    # Сохраняем вопрос в состоянии
    await state.update_data(question=message.text)
    
    # Отправляем сообщение с клавиатурой выбора действий
    await message.answer(
        "Отлично! Теперь вы можете выбрать карты для гадания или вернуться в главное меню.",
        reply_markup=get_question_actions_keyboard(message.text)
    )
    await state.set_state(QuestionStates.waiting_for_cards)

@router.message(F.text == "⬅️ Вернуться назад")
async def back_to_main_menu(message: types.Message, state: FSMContext):
    """
    Обработчик кнопки "Вернуться назад"
    """
    await state.clear()
    await state.set_state(QuestionStates.main_menu)
    await message.answer(
        "Вы вернулись в главное меню.",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "🃏 Выбрать карты")
async def handle_choose_cards(message: types.Message, session: AsyncSession, state: FSMContext):
    """
    Обработчик кнопки выбора карт
    """
    # Проверяем, существует ли пользователь
    user = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    )
    user = user.scalar_one_or_none()
    
    if not user:
        await message.answer("Пожалуйста, сначала нажмите /start")
        return
    
    # Проверяем, есть ли у пользователя оставшиеся попытки
    if user.readings_remaining <= 0:
        await message.answer("У вас нет оставшихся попыток. Пожалуйста, приобретите подписку.")
        return
    
    # Получаем вопрос из состояния
    data = await state.get_data()
    question = data.get("question")
    
    if not question:
        await message.answer("Пожалуйста, сначала задайте вопрос.")
        return
    
    # Получаем данные о картах
    cards = get_random_tarot_cards()
    cards_json = json.dumps(cards)
    encoded_cards = urllib.parse.quote(cards_json)
    encoded_question = urllib.parse.quote(question)
    
    # Создаем новое гадание
    reading = Reading(
        user_id=user.id,
        question=question,
        interpretation="",  # Добавляем пустую строку как значение по умолчанию
        created_at=datetime.utcnow()
    )
    
    session.add(reading)
    await session.commit()
    
    # Уменьшаем количество оставшихся попыток
    user.readings_remaining -= 1
    await session.commit()
    
    # Создаем клавиатуру с webapp кнопкой
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(
                text="Выбрать карты",
                web_app=types.WebAppInfo(url=f"{WEBAPP_URL}?cards={encoded_cards}&question={encoded_question}")
            )]
        ],
        resize_keyboard=True
    )
    
    # Отправляем клавиатуру
    await message.answer(reply_markup=keyboard)

@router.message(QuestionStates.processing_reading)
async def process_reading(message: types.Message, state: FSMContext, session: AsyncSession):
    """
    Обработчик данных от веб-приложения
    """
    if not message.web_app_data:
        await message.answer(
            "Пожалуйста, используйте кнопку для выбора карт.",
            reply_markup=get_main_keyboard()
        )
        return
    
    try:
        # Получаем данные из веб-приложения
        data = json.loads(message.web_app_data.data)
        selected_cards = data.get('selected_cards', [])
        
        if not selected_cards or len(selected_cards) != 3:
            await message.answer(
                "Произошла ошибка при получении выбранных карт. Пожалуйста, попробуйте снова.",
                reply_markup=get_main_keyboard()
            )
            return
        
        # Получаем вопрос из состояния
        state_data = await state.get_data()
        question = state_data.get("question")
        
        if not question:
            await message.answer(
                "Произошла ошибка. Пожалуйста, попробуйте задать вопрос снова.",
                reply_markup=get_main_keyboard()
            )
            await state.set_state(QuestionStates.main_menu)
            return
        
        # Формируем промпт для OpenAI
        cards_info = "\n".join([
            f"Карта {i+1}: {card['name']['ru']} - {card['meaning']['ru']}"
            for i, card in enumerate(selected_cards)
        ])
        
        prompt = f"""Вопрос: {question}

Выбранные карты:
{cards_info}

Пожалуйста, дайте подробную интерпретацию расклада, учитывая значение каждой карты и их взаимосвязь."""
        
        # Получаем интерпретацию от OpenAI
        interpretation = await get_interpretation_from_openai(prompt)
        
        # Обновляем запись в базе данных
        reading = await session.execute(
            select(Reading).where(
                Reading.user_id == message.from_user.id,
                Reading.question == question,
                Reading.interpretation == ""
            ).order_by(Reading.created_at.desc())
        )
        reading = reading.scalar_one_or_none()
        
        if reading:
            reading.interpretation = interpretation
            await session.commit()
        
        # Отправляем результат пользователю
        await message.answer(
            f"🔮 Ваш вопрос: {question}\n\n"
            f"📜 Интерпретация:\n{interpretation}",
            reply_markup=get_main_keyboard()
        )
        
    except Exception as e:
        logger.error(f"Ошибка при обработке данных от веб-приложения: {str(e)}")
        await message.answer(
            "Произошла ошибка при обработке результатов. Пожалуйста, попробуйте позже.",
            reply_markup=get_main_keyboard()
        )
    
    await state.set_state(QuestionStates.main_menu)

@router.message(QuestionStates.main_menu)
async def handle_main_menu(message: types.Message, session: AsyncSession):
    """
    Обработчик сообщений в главном меню
    """
    # Если это не текстовое сообщение или это кнопка, игнорируем
    if not message.text or message.text in ["🎴 Задать вопрос", "🃏 Выбрать карты", "⬅️ Вернуться назад"]:
        return
    
    # Проверяем, существует ли пользователь
    user = await session.execute(
        select(User).where(User.telegram_id == message.from_user.id)
    )
    user = user.scalar_one_or_none()
    
    if not user:
        await message.answer("Пожалуйста, сначала нажмите /start")
        return
    
    # Проверяем, есть ли у пользователя оставшиеся попытки
    if user.readings_remaining <= 0:
        await message.answer("У вас нет оставшихся попыток. Пожалуйста, приобретите подписку.")
        return
    
    # Проверяем длину вопроса
    if not message.text:
        await message.answer("Пожалуйста, введите текстовый вопрос.")
        return

    if len(message.text) < TAROT_SETTINGS["min_question_length"]:
        await message.answer(f"Вопрос слишком короткий. Минимальная длина: {TAROT_SETTINGS['min_question_length']} символов.")
        return
    
    if len(message.text) > TAROT_SETTINGS["max_question_length"]:
        await message.answer(f"Вопрос слишком длинный. Максимальная длина: {TAROT_SETTINGS['max_question_length']} символов.")
        return
    
    # Создаем новое гадание
    reading = Reading(
        user_id=user.id,
        question=message.text,
        created_at=datetime.utcnow()
    )
    
    session.add(reading)
    await session.commit()
    
    # Уменьшаем количество оставшихся попыток
    user.readings_remaining -= 1
    await session.commit()
    
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Выбрать карты",
                    web_app={"url": f"{WEBAPP_URL}/index.html"}
                )
            ]
        ]
    )
    
    await message.answer(
        "Нажмите на кнопку ниже, чтобы открыть мини-приложение для выбора карт Таро:",
        reply_markup=keyboard
    )

@router.message(StateFilter(QuestionStates.choosing_cards))
async def choose_cards(message: types.Message, state: FSMContext):
    """Обработчик выбора карт"""
    try:
        # Получаем данные из состояния
        data = await state.get_data()
        question = data.get('question')
        
        if not question:
            await message.answer("❌ Произошла ошибка. Пожалуйста, начните гадание заново.")
            await state.clear()
            return
            
        # Создаем кнопку для открытия веб-приложения
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Открыть веб-приложение",
                        web_app=WebAppInfo(url=f"{WEBAPP_URL}?question={urllib.parse.quote(question)}")
                    )
                ]
            ]
        )
        
        # Отправляем сообщение с кнопкой
        await message.answer(
            "Открываю веб-приложение для выбора карт...",
            reply_markup=keyboard
        )
        
    except Exception as e:
        logger.error(f"Ошибка при выборе карт: {str(e)}")
        await message.answer("❌ Произошла ошибка при открытии веб-приложения. Пожалуйста, попробуйте позже.")
        await state.clear() 