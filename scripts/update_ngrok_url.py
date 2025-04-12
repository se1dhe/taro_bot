#!/usr/bin/env python3
"""
Скрипт для обновления URL ngrok в .env файле
"""
import os
import time
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv, set_key

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_ngrok_url(max_retries: int = 10, delay: int = 5) -> str:
    """
    Получает публичный URL из ngrok API
    
    :param max_retries: Максимальное количество попыток
    :param delay: Задержка между попытками в секундах
    :return: Публичный URL
    """
    for attempt in range(max_retries):
        try:
            response = requests.get("http://ngrok:4040/api/tunnels")
            data = response.json()
            
            if "tunnels" in data and len(data["tunnels"]) > 0:
                public_url = data["tunnels"][0]["public_url"]
                logger.info(f"Получен публичный URL: {public_url}")
                return public_url
            
            logger.warning(f"Попытка {attempt + 1}/{max_retries}: URL не найден")
            time.sleep(delay)
            
        except Exception as e:
            logger.error(f"Ошибка при получении URL: {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise Exception("Не удалось получить URL ngrok после всех попыток")
    
    raise Exception("Не удалось получить URL ngrok")

def update_env_file(ngrok_url: str) -> None:
    """
    Обновляет URL в .env файле
    
    :param ngrok_url: Новый URL ngrok
    """
    env_path = Path(".env")
    if not env_path.exists():
        raise FileNotFoundError("Файл .env не найден")
    
    # Загружаем текущие переменные
    load_dotenv(env_path)
    
    # Обновляем URL
    set_key(env_path, "WEBAPP_URL", ngrok_url)
    logger.info(f"URL обновлен в .env: {ngrok_url}")

def rebuild_and_restart_containers() -> None:
    """
    Пересобирает и перезапускает контейнеры
    """
    logger.info("Пересборка и перезапуск контейнеров...")
    os.system("docker-compose down")
    os.system("docker-compose up --build -d")
    logger.info("Контейнеры перезапущены")

def main():
    try:
        # Ждем запуска ngrok
        logger.info("Ожидание запуска ngrok...")
        time.sleep(10)
        
        # Получаем URL
        ngrok_url = get_ngrok_url()
        
        # Обновляем .env
        update_env_file(ngrok_url)
        
        # Пересобираем и перезапускаем контейнеры
        rebuild_and_restart_containers()
        
        logger.info("Процесс завершен успешно")
        
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
        exit(1)

if __name__ == "__main__":
    main() 