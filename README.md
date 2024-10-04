# Lyceum

[![pipeline status](https://gitlab.crja72.ru/django/2024/autumn/course/students/286651-ya.vkarsten-course-1187/badges/main/pipeline.svg)](https://gitlab.crja72.ru/django/2024/autumn/course/students/286651-ya.vkarsten-course-1187/-/commits/main)

## Запуск Dev-режима

### Linux/Unix

1. Создать виртуальное окружение:
```bash
python3 -m venv venv
```

2. Активировать виртуальное окружение:
```bash
source venv/bin/activate
```

3. Установить необходимые зависимости:
```bash
pip install -r requirements/dev.txt
```

4. Перейти в папку проекта:
```bash
cd lyceum
```

5. Сохранить переменные окружения в файл ```.env```:
```bash
echo "DEBUG=true" >> .env
echo "SECRET_KEY=your_secret_key" >> .env
echo "ALLOWED_HOSTS=example.com,yourdomain.com" >> .env
```

6. Запустить сервер:
```bash
python manage.py runserver
```

### Windows
1. Создать виртуальное окружение:
```bash
python -m venv venv
```

2. Активировать виртуальное окружение:
```bash
venv\Scripts\activate.bat
```

3. Установить необходимые зависимости:
```bash
pip install -r requirements/dev.txt
```

4. Перейти в папку проекта:
```bash
cd lyceum
```

5. Сохранить переменные окружения в файл ```.env```:
```bash
echo DEBUG=true >> .env
echo SECRET_KEY=your_secret_key >> .env
echo ALLOWED_HOSTS=example.com,yourdomain.com >> .env
```

6. Запустить сервер:
```bash
python manage.py runserver
```
