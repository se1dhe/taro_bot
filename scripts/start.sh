#!/bin/bash

# Останавливаем все контейнеры
echo "Останавливаем контейнеры..."
docker-compose down -v

# Удаляем все образы
echo "Удаляем старые образы..."
docker-compose rm -f

# Удаляем все неиспользуемые образы
echo "Удаляем неиспользуемые образы..."
docker image prune -f

# Собираем образы без кеширования
echo "Собираем образы без кеширования..."
docker-compose build --no-cache

# Запускаем контейнеры
echo "Запускаем контейнеры..."
docker-compose up -d

# Ждем запуска ngrok
echo "Ожидание запуска ngrok..."
sleep 10

# Запускаем скрипт обновления URL
echo "Обновляем URL ngrok..."
python3 scripts/update_ngrok_url.py

# Показываем логи
echo "Показываем логи..."
docker-compose logs -f 