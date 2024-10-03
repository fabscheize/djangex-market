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
$ pip3 install -r requirements.txt
```

4. Задать переменную окуржения ```DJANGO_DEBUG``` в значение ```True```:
```bash
$ export DJANGO_DEBUG=True
```

5. Запустить сервер:
```bash
$ python3 lyceum/manage.py runserver
```
