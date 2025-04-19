"""
Конфигурационный файл для бота
"""
import logging
from dotenv import load_dotenv
import os

# Настройка логгера
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
logger.info(f"Загрузка переменных окружения из файла: {env_path}")
load_dotenv(env_path)

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

# Промты для расклада на месяц
MONTHLY_READING_PROMPT_RU = """Вы — профессиональный таролог, который интерпретирует карты клиента глубоко, нюансировано и практично. Вы связываете карты воедино, создавая интерпретацию, которая фокусируется на том, как карты влияют друг на друга, учитывая их позиции для добавления контекста, вместо того чтобы интерпретировать каждую карту по отдельности. Например, центральная карта может быть значительно усилена (или ослаблена) картами слева и справа. Карты будут выложены слева — в центре — справа.

Вы также можете указывать на важные символы или астрологические связи в картах (их зодиакальных управителей или соответствующие астрологические положения) и на то, как они влияют друг на друга, если это добавляет ценности толкованию. В целом, вы превосходно создаёте нарратив из карт, который резонирует с ситуацией клиента.

Вы избегаете общих, универсальных советов и делаете всё возможное, чтобы действительно углубиться в конкретную ситуацию клиента, даже предполагая, когда это необходимо (на основе нарратива показанных карт)."""

MONTHLY_READING_PROMPT_EN = """You are a professional Tarot reader who interprets the client's cards with depth, nuance, and practical clarity. You tie the cards together to create an interpretation that focuses on how the cards impact each other, taking their positions into consideration to add context, rather than interpreting each card individually. For example, the card in the center may be significantly influenced (or weakened) by the left and right cards. The cards will be laid as Left - Center - Right.
You may also point out any important symbols or astrological connections in the cards (their zodiac rulers or corresponding astrological placements) and how they influence each other, if it adds value to the reading. Overall you excel at creating a narrative from the cards that resonates with the client's situation.
You stray from generic, one-size-fits-all advice and do your best to really dig into the client's particular situation, even speculating when necessary (based on the narrative of the cards shown)."""

# Настройки базы данных
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "tarot_bot")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")

# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")

# Настройки тарифов (в рублях)
TARIFF_SMALL_PRICE_RUB = int(os.getenv("TARIFF_SMALL_PRICE_RUB", "99"))
TARIFF_SMALL_READINGS = int(os.getenv("TARIFF_SMALL_READINGS", "3"))
TARIFF_SMALL_DURATION = int(os.getenv("TARIFF_SMALL_DURATION", "30"))

TARIFF_MEDIUM_PRICE_RUB = int(os.getenv("TARIFF_MEDIUM_PRICE_RUB", "199"))
TARIFF_MEDIUM_READINGS = int(os.getenv("TARIFF_MEDIUM_READINGS", "7"))
TARIFF_MEDIUM_DURATION = int(os.getenv("TARIFF_MEDIUM_DURATION", "30"))

TARIFF_UNLIMITED_PRICE_RUB = int(os.getenv("TARIFF_UNLIMITED_PRICE_RUB", "499"))
TARIFF_UNLIMITED_DURATION = int(os.getenv("TARIFF_UNLIMITED_DURATION", "30"))

# Настройки тарифов (в звёздах)
TARIFF_SMALL_PRICE_STARS = int(os.getenv("TARIFF_SMALL_PRICE_STARS", "10"))
TARIFF_MEDIUM_PRICE_STARS = int(os.getenv("TARIFF_MEDIUM_PRICE_STARS", "20"))
TARIFF_UNLIMITED_PRICE_STARS = int(os.getenv("TARIFF_UNLIMITED_PRICE_STARS", "50"))

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

# WebApp settings
WEBAPP_URL = os.getenv("WEBAPP_URL")
if not WEBAPP_URL:
    raise ValueError("WEBAPP_URL не найден в переменных окружения")
logger.info(f"WEBAPP_URL: {WEBAPP_URL}")

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

# Настройки Robokassa
ROBOKASSA_LOGIN = os.getenv("ROBOKASSA_LOGIN")
if not ROBOKASSA_LOGIN:
    raise ValueError("ROBOKASSA_LOGIN не найден в переменных окружения")

ROBOKASSA_PASSWORD1 = os.getenv("ROBOKASSA_PASSWORD1")
if not ROBOKASSA_PASSWORD1:
    raise ValueError("ROBOKASSA_PASSWORD1 не найден в переменных окружения")

ROBOKASSA_PASSWORD2 = os.getenv("ROBOKASSA_PASSWORD2")
if not ROBOKASSA_PASSWORD2:
    raise ValueError("ROBOKASSA_PASSWORD2 не найден в переменных окружения")

ROBOKASSA_TEST_MODE = os.getenv("ROBOKASSA_TEST_MODE", "false").lower() == "true"

# URL для перенаправления после оплаты
ROBOKASSA_SUCCESS_URL = os.getenv("ROBOKASSA_SUCCESS_URL", f"{WEBAPP_URL}/robokassa/success")
ROBOKASSA_FAIL_URL = os.getenv("ROBOKASSA_FAIL_URL", f"{WEBAPP_URL}/robokassa/fail")

# Настройки базы данных для SQLAlchemy
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Настройки Redis для aioredis
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0" 