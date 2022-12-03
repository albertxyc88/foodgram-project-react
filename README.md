![foodgram workflow](https://github.com/albertxyc88/foodgram-project-react/actions/workflows/main.yml/badge.svg)

http://albertxyc.ddns.net/ or http://51.250.93.230/

admin user: test@gmail.com / Qwerty!!!

# Проект Foodgram - Продуктовый помощник
## Описание
На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии
Python 3.7, Django 2.2, DRF 3.12, gunicorn 20.0.4, nginx, PostgreSQL, github actions.

## Принцип работы
Локально вносятся изменения в существующий проект, при каджом push на github срабатывает action:
 - проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8).
 - сборка и доставка докер-образа для контейнера web на Docker Hub;
 - автоматический деплой проекта на боевой сервер;
 - отправка уведомления в Telegram о том, что процесс деплоя успешно завершился.

## Порядок установки
 
Сделать fork проекта к себе в профиль, 

подготовить сервер с доступом по ssh, 

подготовить базу данных для проекта,

в телеграме через @userinfobot - узнать свой ID для получения сообщения об успешном деплое на сервере, 

завести бота в телеграм @Botfather 

На GitHUB на вкладке settings этого репозитария - secrets задать переменные

DB_ENGINE - указат тип вашей БД для использования в Django - например: django.db.backends.postgresql

DB_HOST - db - название контейнера в docker-compose 

DB_NAME - название БД

DB_PORT - порт подключения к БД

DOCKER_PASSWORD -  пароль для подключения к docker HUB

DOCKER_USERNAME - пользователь для подключения к docker HUB

HOST - адрес боевого сервера (ip)

PASSPHRASE - указать если при создании ssh-ключа вы использовали фразу-пароль

POSTGRES_PASSWORD - пароль для доступа к БД

POSTGRES_USER - имя пользователя имеющего доступ к БД

SECRET_KEY - Django secret key для settings.py

SSH_KEY - Скопируйте приватный ключ с компьютера, имеющего доступ к боевому серверу:  cat ~/.ssh/id_rsa

TELEGRAM_TO - id кому отправлять результат деплоя на сервере.

TELEGRAM_TOKEN - токен бота телеграм

USER - имя пользователя для подключения к серверу по ssh

далее в файле .github/workflows/main.yml поправьте раздел - name: Push to Docker Hub

`tags: your_dockerhub_username/foodgrambackend:latest`

и в файле infra/docker-compose.yaml 

```
web:
    image: your_dockerhub_username/foodgrambackend:latest
```

в файле infra/nginx/default.conf укажите публичный адрес вашего боевого сервера. 

Скопируйте файлы docker-compose.yaml и nginx/default.conf из вашего проекта на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf соответственно.

Сделайте push в main ветку на GitHUB во вкладке actions отследите правильность выполнения всех этапов и успешный деплой на сервере.

Переходим на сайт и производим регистрацию пользователя.

При необходимости можно загрузить вложенную базу ингредиентов командой:

`sudo docker-compose exec backend python manage.py load_db_data`
