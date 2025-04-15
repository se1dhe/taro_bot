"""
Конфигурационный файл для бота
"""
import logging
from dotenv import load_dotenv
import os
from src.utils.ngrok import get_ngrok_url

# Настройка логгера
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

# Настройки бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в переменных окружения")

BOT_USERNAME = os.getenv("BOT_USERNAME")
ADMIN_IDS = [int(id) for id in os.getenv("ADMIN_IDS", "").split(",") if id]

# Настройки OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден в переменных окружения")

OPENAI_MODEL = os.getenv("OPENAI_MODEL")

# Промпты для генерации ответов
TAROT_PROMPT_RU = os.getenv("TAROT_PROMPT_RU")
TAROT_PROMPT_EN = os.getenv("TAROT_PROMPT_EN")

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Настройки Redis
REDIS_URL = os.getenv("REDIS_URL")

# Настройки Robokassa
ROBOKASSA_LOGIN = os.getenv("ROBOKASSA_LOGIN")
ROBOKASSA_PASSWORD1 = os.getenv("ROBOKASSA_PASSWORD1")
ROBOKASSA_PASSWORD2 = os.getenv("ROBOKASSA_PASSWORD2")
ROBOKASSA_TEST_MODE = os.getenv("ROBOKASSA_TEST_MODE", "True").lower() == "true"

# Настройки тарифов
TARIFF_SMALL_PRICE_RUB = int(os.getenv("TARIFF_SMALL_PRICE"))
TARIFF_SMALL_PRICE_STARS = int(os.getenv("TARIFF_SMALL_PRICE_STARS"))
TARIFF_SMALL_READINGS = int(os.getenv("TARIFF_SMALL_READINGS"))
TARIFF_SMALL_DURATION = int(os.getenv("TARIFF_SMALL_DURATION"))

TARIFF_MEDIUM_PRICE_RUB = int(os.getenv("TARIFF_MEDIUM_PRICE"))
TARIFF_MEDIUM_PRICE_STARS = int(os.getenv("TARIFF_MEDIUM_PRICE_STARS"))
TARIFF_MEDIUM_READINGS = int(os.getenv("TARIFF_MEDIUM_READINGS"))
TARIFF_MEDIUM_DURATION = int(os.getenv("TARIFF_MEDIUM_DURATION"))

TARIFF_UNLIMITED_PRICE_RUB = int(os.getenv("TARIFF_UNLIMITED_PRICE"))
TARIFF_UNLIMITED_PRICE_STARS = int(os.getenv("TARIFF_UNLIMITED_PRICE_STARS"))
TARIFF_UNLIMITED_DURATION = int(os.getenv("TARIFF_UNLIMITED_DURATION"))

# Настройки Таро
TAROT_READINGS_PER_DAY = int(os.getenv("TAROT_READINGS_PER_DAY"))
TAROT_READING_PRICE = int(os.getenv("TAROT_READING_PRICE"))
FREE_READINGS_COUNT = int(os.getenv("FREE_READINGS_COUNT"))
REFERRAL_BONUS_READINGS = int(os.getenv("REFERRAL_BONUS_READINGS"))

# Настройки реферальной системы
TAROT_SETTINGS = {
    "free_readings_count": FREE_READINGS_COUNT,
    "referral_bonus_readings": REFERRAL_BONUS_READINGS,
    "min_question_length": 10,
    "max_question_length": 500
}

# Настройки локализации
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE")
SUPPORTED_LANGUAGES = os.getenv("SUPPORTED_LANGUAGES").split(",")

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

# WebApp settings
try:
    WEBAPP_URL = get_ngrok_url()
except Exception as e:
    logger.error(f"Ошибка при получении URL от ngrok: {e}")
    WEBAPP_URL = os.getenv("WEBAPP_URL")

# Настройки ngrok
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN") 