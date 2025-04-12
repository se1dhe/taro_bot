"""
Утилиты для работы с OpenAI API
"""
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def get_interpretation_from_openai(prompt: str) -> str:
    """
    Получает интерпретацию расклада от OpenAI
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Вы - опытный таролог, который дает точные и подробные интерпретации раскладов Таро. Ваши ответы всегда структурированы, понятны и содержат конкретные рекомендации."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Ошибка при получении интерпретации от OpenAI: {str(e)}")
        return "Извините, произошла ошибка при получении интерпретации. Пожалуйста, попробуйте позже." 