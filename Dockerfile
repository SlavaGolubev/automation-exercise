# 1. Берем официальный образ Playwright с Python (Ubuntu 22.04)
FROM mcr.microsoft.com/playwright/python:v1.64.1-jammy

# 2. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 3. Копируем файл зависимостей
COPY requirements.txt .

# 4. Устанавливаем зависимости (без кэша, чтобы уменьшить размер образа)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь остальной код проекта в контейнер
COPY . .

# 6. Команда, которая выполнится при запуске контейнера
CMD ["pytest", "tests/", "-v", "--alluredir=allure-results"]