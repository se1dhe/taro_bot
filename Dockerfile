FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl netcat-traditional postgresql-client g++ build-essential && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g http-server && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаем директорию для статических файлов
RUN mkdir -p /app/webapp/static/images

# Копируем статические файлы
COPY src/webapp/static/images /app/webapp/static/images/

ENV PYTHONPATH=/app

CMD ["sh", "-c", "cd src/webapp && http-server -p 8000 & cd /app && python src/main.py"] 