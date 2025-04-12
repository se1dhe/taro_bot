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
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]

# Настройки OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден в переменных окружения")

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# Промпты для генерации ответов
TAROT_PROMPT_RU = os.getenv("TAROT_PROMPT_RU")
TAROT_PROMPT_EN = os.getenv("TAROT_PROMPT_EN")

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@db:5432/tarot_bot")

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
    "min_question_length": 10,
    "max_question_length": 500,
    "cards_per_reading": 3,
    "free_readings_count": 3  # Количество бесплатных гаданий для новых пользователей
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
    WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:8000")

# Tarot settings
TAROT_SETTINGS = {
    "min_question_length": 10,
    "max_question_length": 500,
    "cards_per_reading": 3,
    "free_readings_count": 3  # Количество бесплатных гаданий для новых пользователей
}
SUPPORTED_LANGUAGES = ["ru", "en"] 