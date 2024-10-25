# Lyceum

[![pipeline status](https://gitlab.crja72.ru/django/2024/autumn/course/students/286651-ya.vkarsten-course-1187/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/autumn/course/students/286651-ya.vkarsten-course-1187/-/commits/main)

## Содержание
- [Зависимости](#зависимости)
- [Установка](#установка)
- [Запуск сервера](#запуск-сервера)
- [Локальная разработка](#локальная-разработка)
- [Тестирование](#тестирование)
- [ER-диаграмма](#er-диаграмма)

## Зависимости

- Python 3.9 или выше

## Установка

1. Клонирование репозитория:
```bash
git clone https://gitlab.crja72.ru/django/2024/autumn/course/students/286651-ya.vkarsten-course-1187 && cd 286651-ya.vkarsten-course-1187
```

2. Создание виртуального окружения:

- Linux/MacOS
```bash
python3 -m venv venv
```
- Windows
```bash
python -m venv venv
```

3. Активация виртуального окружения:

- Linux/MacOS
```bash
source venv/bin/activate
```
- Windows
```bash
venv\Scripts\activate.bat
```

## Запуск

Необходимо выполнить команды из корневой директории проекта:

1. Установка зависимостей:
```bash
pip install -r requirements/prod.txt
```

2. Переход в директорию проекта:
```bash
cd lyceum
```

3. Примемение миграций:
```bash
python manage.py migrate
```

4. Запуск сервера:
```bash
python manage.py runserver
```

## Локальная разработка

Необходимо выполнить команды из корневой директории проекта:

1. Установка зависимостей для разработки:
```bash
pip install -r requirements/dev.txt
```
2. Переход в директорию проекта:
```bash
cd lyceum
```

3. Редактирование (при необходимости) переменных окружения в файле ```.env.example``` и копирование их в файл ```.env```:

- Linux/MacOS
```bash
cp .env.example .env
```
- Windows
```bash
copy .env.example .env
```

4. Для запуска можно использовать демонстрационную БД – для это необходимо скопировать ее из файла:

- Linux/MacOS
```bash
cp demo_db.sqllite3 db.sqllite3
```
- Windows
```bash
copy demo_db.sqllite3 db.sqllite3
```

5. Примемение миграций:
```bash
python manage.py migrate
```

6. Запуск сервера:
```bash
python manage.py runserver
```

Для админки:

- логин ```admin```
- пароль ```admin```

## Тестирование

Необходимо выполнить команды из корневой директории проекта:

1. Установка зависимостей для тестирования:
```bash
pip install -r requirements/test.txt
```

2. Переход в директорию проекта:
```bash
cd lyceum
```

3. Запуск тестов:
```bash
python manage.py test
```

## ER-диаграмма

ER-диаграмма базы данных приложения ```Catalog```:

![ERD](./ER.jpg)
