#!/bin/bash



# Ожидание, пока база данных будет готова
until pg_isready -h db -p 5432; do
  echo "Ожидание базы данных..."
  sleep 2
done

# Выполнение миграций Alembic
alembic upgrade head

# Запуск сервера Gunicorn
exec gunicorn  --workers 4 --bind 0.0.0.0:5000 app.apps:app