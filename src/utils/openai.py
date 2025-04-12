"""
Утилиты для работы с OpenAI API
"""
import os
import logging
from openai import AsyncOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL, TAROT_PROMPT_RU, TAROT_PROMPT_EN

# Создаем клиент OpenAI
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

def format_interpretation(text: str) -> str:
    """
    Форматирует текст интерпретации в Markdown
    """
    # Добавляем отступы для лучшей читаемости
    text = text.replace("\n\n", "\n\n  ")
    
    return text

async def get_interpretation_from_openai(cards: list, question: str, language: str = "ru") -> str:
    """
    Получает интерпретацию расклада от OpenAI.
    
    Args:
        cards: Список выбранных карт
        question: Вопрос пользователя
        language: Язык ответа (ru/en)
        
    Returns:
        str: Интерпретация расклада в формате Markdown
    """
    try:
        # Выбираем промпт в зависимости от языка
        prompt = TAROT_PROMPT_RU if language == "ru" else TAROT_PROMPT_EN
        
        # Формируем сообщение для OpenAI
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"Вопрос: {question}\n\nВыбранные карты: {', '.join(cards)}"}
        ]
        
        # Получаем ответ от OpenAI
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            top_p=0.9,
            frequency_penalty=0.5,
            presence_penalty=0.5
        )
        
        # Форматируем ответ
        interpretation = response.choices[0].message.content
        formatted_interpretation = format_interpretation(interpretation)
        
        return formatted_interpretation
        
    except Exception as e:
        logging.error(f"Ошибка при получении интерпретации от OpenAI: {str(e)}")
        return "Извините, произошла ошибка при генерации интерпретации. Пожалуйста, попробуйте позже." 