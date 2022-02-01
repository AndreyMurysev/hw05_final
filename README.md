# Блог YaMyGame
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)


## Описание
Проект задеплоен на python-anywhere, посмотреть и протестировать  здесь:
[YaMyGame](http://futuresenior.pythonanywhere.com/)

YaMyGame - это социальная сеть для публикации постов с играми, разработана для изучения фреймворка Django.

## Возможности для пользователей: 

- регистрироваться и логиниться, восстанавливать пароль по почте
- создавать, редактировать, удалять свой профиль (аватар, описание)
- создавать, редактировать, удалять и просматривать свои группы и вступать в созданные другими пользователями
- создавать, редактировать, удалять свои записи
- просматривать страницы других пользователей
- комментировать записи других авторов
- подписываться на авторов, просматривать список подписок и подписчиков
- cтавить и убирать лайки на публикации

## Возможности для администратора: 

Модерация записей осуществляется через встроенную панель администратора

## Установка проекта:
- Клонировать репозиторий GitHub:
[https://github.com/AndreyMurysev/hw05_final](https://github.com/AndreyMurysev/hw05_final) 

- Создайте и активируйте виртуальное окружение
```
python -m venv venv  
source activate 
```

Установите требуемые зависимости
```
pip install -r requirements.txt
```

- Сделать миграции, создать суперпользователя и собрать статику:
```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --no-input
```

- Запустите django-сервер
```
python manage.py runserver
```
**Приложение будет доступно по адресу:** _http://127.0.0.1:8000/_

### Автор проекта:
_Мурысев Андрей_  
**email:** _andreimurysev@yandex.ru_  
**telegram:** _@andrey_murysev_  
