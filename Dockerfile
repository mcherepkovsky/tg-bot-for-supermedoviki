# Используем официальный образ Python как базовый
FROM python:3.12-slim

# Устанавливаем зависимости
RUN apt-get update \
    && apt-get install -y \
       build-essential \
       libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости
RUN poetry install --no-root

# Копируем код приложения
COPY tg-bot-for-supermedoviki/tg_bot_for_supermedoviki /app/tg_bot_for_supermedoviki

# Устанавливаем переменную окружения для Poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true

# Команда для запуска приложения
CMD ["poetry", "run", "python", "tg_bot_for_supermedoviki/bot.py"]
