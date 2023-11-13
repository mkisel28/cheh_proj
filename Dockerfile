# Использование официального образа Python
FROM python:3.9

# Установка рабочей директории в контейнере
WORKDIR /usr/src/app

# Копирование файлов проекта и зависимостей в контейнер
COPY . .

# Установка необходимых библиотек
RUN pip install --no-cache-dir pyTelegramBotAPI

# Команда для запуска бота
CMD ["python", "./your_script.py"]