# Foodrgam

### Что ты такое?

Дипломный проект в Яндекс.Практикуме.

Онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

### Как запустить?

Склонируйте репозиторий:

```bash
https://github.com/sh4rpy/foodgram-project.git
```

Создайте файл .env в одной директории с файлом settings.py. Создайте в нем переменную окружения  SECRET_KEY, которой присвойте скопированный ключ с [сайта генерации ключей](https://djecrety.ir). Далее добавьте переменные для работы с базой данных. Выглядеть файл должен так:

```python
SECRET_KEY=скопированный_ключ
DB_ENGINE=django.db.backends.postgresql
DB_NAME=имя_базы
DB_USER=юзернейм
DB_PASSWORD=пароль
DB_HOST=db # имя контейнера базы данных
DB_PORT=порт
```

Запустите **docker-compose** командной:

```bash
docker-compose up
```

Сервис станет доступен по адресу [http://0.0.0.0:5555](http://0.0.0.0:5555/).

### Потыкать можно тут:

[Рецепты](http://84.201.158.254)