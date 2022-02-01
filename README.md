# Блог YaMyGame
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![SQLite](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)

## Описание
Проект задеплоен на python-anywhere, посмотреть и протестировать  здесь:
[YaMyGame](http://futuresenior.pythonanywhere.com/)

YaMyGame - это социальная сеть для публикации постов с играми, разработана для изучения фреймворка Django.

Возможности для пользователей: 

- регистрироваться и логиниться, восстанавливать пароль по почте
- создавать, редактировать, удалять свой профиль (аватар, описание)
- создавать, редактировать, удалять и просматривать свои группы и вступать в созданные другими пользователями
- создавать, редактировать, удалять свои записи
- просматривать страницы других пользователей
- комментировать записи других авторов
- подписываться на авторов, просматривать список подписок и подписчиков
- cтавить и убирать лайки на публикации

Модерация записей осуществляется через встроенную панель администратора
Используемые технологии
Django 2.2
Python 3.8
SQLite
HTML/CSS
Установка проекта:
Клонируйте данный репозиторий
git clone https://github.com/Viktrols/blog-yatube-yandex-praktikum.git

Создайте и активируйте виртуальное окружение
python -m venv venv<br>
source ./venv/Scripts/activate  #для Windows
source ./venv/bin/activate      #для Linux и macOS
Установите требуемые зависимости
pip install -r requirements.txt
Примените миграции
python manage.py migrate
Запустите django-сервер
python manage.py runserver
Приложение будет доступно по адресу: http://127.0.0.1:8000/
