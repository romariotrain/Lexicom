# Используем официальный образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
COPY ./app /app
WORKDIR /app


# Копируем зависимости и устанавливаем их
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


# Запускаем приложение без --reload для продакшн
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
