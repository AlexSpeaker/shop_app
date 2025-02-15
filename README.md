# Интернет магазин
___
## Создание и активация виртуального окружения
- sudo apt install python3-virtualenv
- virtualenv venv
- source venv/bin/activate
___
## Установка зависимостей
- Необходимо установить библиотеку **Poetry**: **pip install poetry**
- И выполняем установку всех зависимостей в проекте командой: **poetry install**
___
## Применяем миграции
- Переходим в корень нашего проекта. Далее переходим в папку **shop_app** и выполняем команду: **python manage.py migrate**

## Создание суперпользователя (администратора)
- Переходим в корень нашего проекта. Далее переходим в папку **shop_app** и выполняем команду: **python manage.py createsuperuser**
___
## Запуск проекта
- В папке **shop_app** выполняем команду: **python manage.py runserver**
- Вход в админку **http:/.../admin**
- Swagger документация - **http:/.../api/schema/swagger-ui/**

&#169;AlexSokolov 2025
