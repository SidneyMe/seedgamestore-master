# Seed Game Store

Seed Game Store є веб-додатком, розробленим з використанням Django, призначеним для продажу відеоігор. Він дозволяє користувачам переглядати каталог ігор, придбавати їх та грати в них безпосередньо у браузері. Розробники можуть додавати свої ігри до магазину, встановлювати ціни та відстежувати статистику продажів.

## Основні функції

Для користувачів:
- Перегляд каталогу ігор з фільтрами та сортуванням.
- Детальний перегляд інформації про гру, включаючи опис, знімки екрану та відео.
- Онлайн-покупки ігор.
- Гра в ігри безпосередньо у браузері.
- Створення облікового запису та відстеження історії покупок.

Для розробників:
- Додавання та редагування ігор у каталозі.
- Встановлення цін на ігри.
- Перегляд статистики продажів та доходів.
- REST API для інтеграції з іншими сервісами.

## Технології

#### Backend: Django (Python), SQLite
#### Frontend: HTML, CSS, JavaScript
#### Cloud Storage: Cloudinary
#### Email: Django SMTP
#### Інше: asgiref, certifi, dj-database-url, django-appconf, django-ajax-selects, django-autocomplete-light, django-select2, django-simple-email-confirmation, django-social-share, gunicorn, packaging, pillow, psycopg2-binary, pytz, setuptools, sqlparse, whitenoise

## Встановлення та налаштування

1. Клонуйте репозиторій:
    ```
    git clone https://github.com/your-username/seed-game-store.git
    ```

2. Створіть та активуйте віртуальне середовище:
    ```
    python -m venv venv
    source venv/bin/activate  # Для Linux/macOS
    venv\Scripts\activate  # Для Windows
    ```

3. Встановіть залежності:
    ```
    pip install -r requirements.txt
    ```

4. Застосуйте міграції бази даних:
    ```
    python manage.py migrate
    ```

5. Запустіть сервер розробки:
    ```
    python manage.py runserver
    ```

6. Відкрийте свій браузер та перейдіть за посиланням: http://127.0.0.1:8000/

## Ліцензія

Цей проект поширюється за ліцензією MIT.

## Контактна інформація

Якщо у вас є питання або пропозиції, будь ласка, зв'яжіться з нами:

Email: seedgamestore1@outlook.com