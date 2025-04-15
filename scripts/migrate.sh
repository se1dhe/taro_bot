#!/bin/bash

# Ожидаем, пока база данных будет готова
echo "Ожидаем готовности базы данных..."
while ! pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done
echo "База данных готова!"

# Создаем базу данных, если она не существует
echo "Создаем базу данных..."
psql -h db -U postgres -c "CREATE DATABASE tarot_bot;" || true

# Запускаем миграции
echo "Запускаем миграции..."
cd /app
alembic upgrade 000

echo "Миграции успешно выполнены!" 