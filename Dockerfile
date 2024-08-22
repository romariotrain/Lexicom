# Используем официальный образ Python
FROM python:3.12

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /code/app

# Копируем файл pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock /code/

# Устанавливаем зависимости через Poetry
RUN poetry install --no-root

# Копируем исходный код в контейнер
COPY ./app /code/app


# Запускаем приложение без --reload для продакшн
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
