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

BOT_USERNAME = os.getenv("BOT_USERNAME", "se1dhe_bot")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

# Настройки базы данных
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "bot")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")

# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Настройки Robokassa
ROBOKASSA_LOGIN = os.getenv("ROBOKASSA_LOGIN")
ROBOKASSA_PASSWORD1 = os.getenv("ROBOKASSA_PASSWORD1")
ROBOKASSA_PASSWORD2 = os.getenv("ROBOKASSA_PASSWORD2")
ROBOKASSA_TEST_MODE = os.getenv("ROBOKASSA_TEST_MODE", "1") == "1"

# Настройки тарифов
TARIFF_SMALL_PRICE_STARS = 50  # Цена в звёздах
TARIFF_SMALL_READINGS = 10     # Количество раскладов

TARIFF_MEDIUM_PRICE_STARS = 100  # Цена в звёздах
TARIFF_MEDIUM_READINGS = 25      # Количество раскладов

TARIFF_UNLIMITED_PRICE_STARS = 200  # Цена в звёздах

# Настройки тарифов
TARIFF_SMALL_PRICE_RUB = 99
TARIFF_MEDIUM_PRICE_RUB = 199
TARIFF_UNLIMITED_PRICE_RUB = 299

# Настройки тарифов
TARIFF_SMALL_DURATION = int(os.getenv("TARIFF_SMALL_DURATION", "30"))
TARIFF_MEDIUM_DURATION = int(os.getenv("TARIFF_MEDIUM_DURATION", "30"))
TARIFF_UNLIMITED_DURATION = int(os.getenv("TARIFF_UNLIMITED_DURATION", "30"))

# Настройки Таро
TAROT_READINGS_PER_DAY = int(os.getenv("TAROT_READINGS_PER_DAY", "3"))
TAROT_READING_PRICE = int(os.getenv("TAROT_READING_PRICE", "100"))

# Настройки реферальной системы
TAROT_SETTINGS = {
    "free_readings_count": int(os.getenv("FREE_READINGS_COUNT", "3")),  # Количество бесплатных гаданий для новых пользователей
    "referral_bonus_readings": int(os.getenv("REFERRAL_BONUS_READINGS", "1")),  # Количество бонусных гаданий за каждого реферала
    "min_question_length": 10,  # Минимальная длина вопроса
    "max_question_length": 500  # Максимальная длина вопроса
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

# WebApp settings
try:
    WEBAPP_URL = get_ngrok_url()
except Exception as e:
    logger.error(f"Ошибка при получении URL от ngrok: {e}")
    WEBAPP_URL = os.getenv("WEBAPP_URL", "http://localhost:8000")

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

# Цены тарифов в рублях
TARIFF_SMALL_PRICE_RUB = 99
TARIFF_MEDIUM_PRICE_RUB = 199
TARIFF_UNLIMITED_PRICE_RUB = 299

# Цены тарифов в Stars
TARIFF_SMALL_PRICE_STARS = 50
TARIFF_MEDIUM_PRICE_STARS = 100
TARIFF_UNLIMITED_PRICE_STARS = 200

# Настройки тарифов
TARIFF_SMALL_READINGS = 10
TARIFF_MEDIUM_READINGS = 25

# Настройки тарифов
TARIFF_SMALL_DURATION = 30
TARIFF_MEDIUM_DURATION = 30
TARIFF_UNLIMITED_DURATION = 30

# Настройки ngrok
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN") 