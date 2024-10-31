# # Используем официальный образ Python
# FROM python:3.10-slim
#
# # Устанавливаем рабочую директорию
# WORKDIR /app
#
# # Копируем файлы зависимостей и устанавливаем их
# COPY requirements.txt .
# RUN pip install -r requirements.txt
#
# # Копируем код приложения
# COPY . .
#
#
#
# # Убедитесь, что alembic.ini скопирован
# COPY alembic.ini .
#
# # Установите рабочую директорию для приложения
# # WORKDIR /app/app
#
# # RUN alembic upgrade head
#
#
#
#
#
# WORKDIR /app
#
#
#
# # Команда для запуска приложения с Gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.apps:app"]



#
# FROM python:3.10
#
#
#
# RUN apt-get update && apt-get install -y \
#     postgresql-client \
#     && rm -rf /var/lib/apt/lists/*
#
# RUN mkdir /flask_app
#
# WORKDIR /flask_app
#
#
# COPY requirements.txt .
#
# RUN pip install -r requirements.txt
#
#
# COPY . .
#
# RUN chmod a+x Docker/*.sh
#
# # CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.apps:app"]
# CMD ["sh", "-c", "/flask_app/Docker/app.sh"]



FROM python:3.10

# Установка необходимых пакетов для postgresql
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Создание директории приложения
RUN mkdir /flask_app
WORKDIR /flask_app

# Копирование файла зависимостей и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего кода приложения
COPY . .

# Установка прав на выполнение скриптов
RUN chmod +x /flask_app/Docker/*.sh


# CMD alembic upgrade head && python -m app.main
# CMD ["python", "-m", "app.main"]

# Установка команды по умолчанию
CMD ["sh", "-c", "/flask_app/Docker/app.sh"]