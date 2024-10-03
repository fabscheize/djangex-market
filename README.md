# Проект "Lyceum"

[![pipeline status](https://gitlab.crja72.ru/django/2024/autumn/course/students/286651-ya.vkarsten-course-1187/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/autumn/course/students/286651-ya.vkarsten-course-1187/-/commits/main)

Для запуска проекта в dev-режиме необходимо выполнить следующие команды:

1. Создать виртуальное окружение:
```bash
$ python3 -m venv venv
```

2. Активировать виртуальное окружение:
```bash
$ source venv/bin/activate
```

3. Установить необходимые зависимости:
```bash
$ pip3 install -r requirements/dev.txt
```

4. Задать переменную окуржения ```DJANGO_DEBUG``` в значение ```True```:
```bash
$ export DJANGO_DEBUG=True
```

5. Перейти в папку проекта:
```bash
$ cd lyceum
```

6. Сохранить ключ в переменной окружения:
```bash
$ echo "SECRET_KEY = 'XXX'" >> .env
```

7. Запустить сервер:
```bash
$ python3 manage.py runserver
```
