"""
Конфигурационный файл для бота
"""
from dotenv import load_dotenv
import os
from src.utils.ngrok import get_ngrok_url

# Загрузка переменных окружения
load_dotenv()

# Настройки бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]

# Настройки OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Промпт для генерации ответов
TAROT_PROMPT = os.getenv("TAROT_PROMPT", """
Ты - опытный таролог, работающий с картами Таро Райдера-Уэйта. 
Твоя задача - помочь человеку найти ответы на его вопросы через гадание на картах Таро.

Придерживайся следующих правил:
1. Будь доброжелательным и поддерживающим
2. Используй мудрость карт для предоставления глубоких и полезных инсайтов
3. Избегай негативных предсказаний, вместо этого предлагай конструктивные пути развития
4. Сочетай традиционные значения карт с современным контекстом
5. Помогай человеку увидеть разные перспективы ситуации
6. Вдохновляй на позитивные изменения и личностный рост

Формат ответа:
1. Краткое описание выпавших карт
2. Общее значение расклада
3. Конкретные рекомендации и советы
4. Позитивные аспекты, на которые стоит обратить внимание
5. Возможные пути развития ситуации

Помни: твоя цель - не предсказать будущее, а помочь человеку лучше понять себя и свою ситуацию.
""")

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/tarot_bot")

# Настройки Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

# Настройки Robokassa
ROBOKASSA_LOGIN = os.getenv("ROBOKASSA_LOGIN")
ROBOKASSA_PASSWORD1 = os.getenv("ROBOKASSA_PASSWORD1")
ROBOKASSA_PASSWORD2 = os.getenv("ROBOKASSA_PASSWORD2")
ROBOKASSA_TEST_MODE = os.getenv("ROBOKASSA_TEST_MODE", "True").lower() == "true"

# Настройки тарифов
TARIFF_SMALL_PRICE = int(os.getenv("TARIFF_SMALL_PRICE", "99"))
TARIFF_SMALL_READINGS = int(os.getenv("TARIFF_SMALL_READINGS", "3"))
TARIFF_SMALL_DURATION = int(os.getenv("TARIFF_SMALL_DURATION", "30"))

TARIFF_MEDIUM_PRICE = int(os.getenv("TARIFF_MEDIUM_PRICE", "199"))
TARIFF_MEDIUM_READINGS = int(os.getenv("TARIFF_MEDIUM_READINGS", "10"))
TARIFF_MEDIUM_DURATION = int(os.getenv("TARIFF_MEDIUM_DURATION", "30"))

TARIFF_UNLIMITED_PRICE = int(os.getenv("TARIFF_UNLIMITED_PRICE", "299"))
TARIFF_UNLIMITED_DURATION = int(os.getenv("TARIFF_UNLIMITED_DURATION", "30"))

# Настройки Таро
TAROT_SETTINGS = {
    "new_user_readings": int(os.getenv("NEW_USER_READINGS", "3")),
    "referral_bonus": int(os.getenv("REFERRAL_BONUS", "2")),
    "min_question_length": int(os.getenv("MIN_QUESTION_LENGTH", "10")),
    "max_question_length": int(os.getenv("MAX_QUESTION_LENGTH", "500")),
    "free_readings_count": int(os.getenv("FREE_READINGS_COUNT", "3"))
}

# Настройки локализации
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "ru")
SUPPORTED_LANGUAGES = os.getenv("SUPPORTED_LANGUAGES", "ru,en").split(",")

# Маппинг языков Telegram на поддерживаемые языки
LANGUAGE_MAPPING = {
    "ru": "ru",  # Русский
    "en": "en",  # Английский
    "uk": "ru",  # Украинский -> Русский
    "be": "ru",  # Белорусский -> Русский
    "kk": "ru",  # Казахский -> Русский
    "uz": "ru",  # Узбекский -> Русский
    "az": "ru",  # Азербайджанский -> Русский
    "hy": "ru",  # Армянский -> Русский
    "ka": "ru",  # Грузинский -> Русский
    "de": "en",  # Немецкий -> Английский
    "fr": "en",  # Французский -> Английский
    "es": "en",  # Испанский -> Английский
    "it": "en",  # Итальянский -> Английский
    "pt": "en",  # Португальский -> Английский
    "default": "en"  # Для всех остальных языков -> Английский
}

# Tarot settings
TAROT_READINGS_PER_DAY = 3
TAROT_READING_PRICE = 100  # в рублях

# WebApp settings
try:
    WEBAPP_URL = get_ngrok_url()
except Exception as e:
    logger.error(f"Ошибка при получении URL от ngrok: {e}")
    WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-domain.com")

# Tarot settings
TAROT_SETTINGS = {
    "new_user_readings": 3,  # Количество попыток для нового пользователя
    "referral_bonus": 2,     # Количество дополнительных попыток за реферала
    "min_question_length": 10,  # Минимальная длина вопроса
    "max_question_length": 500,  # Максимальная длина вопроса
    "free_readings_count": 3  # Количество бесплатных попыток
}
SUPPORTED_LANGUAGES = ["ru", "en"] 