from openai import AsyncOpenAI
from src.config import OPENAI_API_KEY, OPENAI_MODEL
import logging

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def get_openai_response(prompt: str) -> str:
    """
    Получает ответ от OpenAI API
    
    Args:
        prompt: Промпт для генерации ответа
    
    Returns:
        str: Сгенерированный ответ
    """
    try:
        response = await client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Ты - опытный таролог, работающий с картами Таро."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от OpenAI: {e}")
        return "Произошла ошибка при генерации ответа. Пожалуйста, попробуйте снова." 