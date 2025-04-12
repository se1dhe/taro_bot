#!/bin/bash

# Ожидаем, пока база данных будет готова
echo "Ожидаем готовности базы данных..."
while ! pg_isready -h db -p 5432 -U postgres; do
  sleep 1
done
echo "База данных готова!"

# Запускаем миграции
echo "Запускаем миграции..."
cd /app
alembic upgrade head

echo "Миграции успешно выполнены!" 