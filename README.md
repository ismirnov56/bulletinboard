<h2 align="center">Bulletine Board by Django</h2>

База данных:
https://app.quickdatabasediagrams.com/#/d/atKUIT

Все модели были приведены к НФБК.
Текущая версия кода закомментирована.

Текущая стадия:
- созданы все модели;
- создана View для регистрация пользователя (покрыто тестами)
    
    python manage.py test .
    
- создана view для активации пользователя
- с помощью докера поднимается брокер и два воркера для отправки активационных писем пользоватедям при регистрации

Запуск с docker:

#### 1) Создание образа

    docker-compose build

##### 2) Запустить контейненр

    docker-compose up
    
##### 3) Создать суперпользователя

    docker exec -it bulletinboard_web_1 python manage.py createsuperuser
    
##### 4) Очистка Базы данных при необходимости

     docker-compose down -v


Запуск без использования docker:

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
    