<h2 align="center">Bulletine Board by Django</h2>

База данных:
https://app.quickdatabasediagrams.com/#/d/atKUIT

Все модели были приведены к НФБК.
Текущая версия кода закомментирована.

Текущая стадия:
- созданы все модели;
- создана View для регистрация пользователя (покрыто тестами)
    
    python manage.py test src.profiles.tests.test_create
    
- активация по email в разработке...

#### 1) Создание окружения

    pip install virtualenv
    python3 -m venv env
    env/bin/activate

##### 2) Установка нужных пакетов

    pip install -r requirements.txt
    
##### 3) Миграции

    python manage.py makemigrations
    python manage.py migrate
    
##### 4) Создание супер пользователя для доступа к Django Admin Panel

     python manage.py createsuperuser
    
##### 5) Запуск приложения
    
    python manage.py runserver
    