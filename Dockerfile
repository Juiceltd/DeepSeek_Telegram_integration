# Используем официальный образ Python (можно выбрать нужную версию, например, 3.9)
FROM python:3.13-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY . /app

# Обновляем pip и устанавливаем зависимости
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000


CMD ["python", "main.py"]