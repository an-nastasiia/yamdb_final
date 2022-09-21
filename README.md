![YaMDb workflow](https://github.com/an-nastasiia/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

# YaMDB

## Что такое YaMDb:

Проект **YaMDb** собирает отзывы пользователей на произведения, поделенные на категории (например, «Литература», «Кино», «Музыка»). Произведению может быть присвоен один или несколько жанров. 

Пользователь может оставить один текстовый отзыв к произведению, имеющемуся в базе данных YaMDb, и оценить его по шкале от одного до десяти. Из средней пользовательской оценки произведения формируется рейтинг этого произведения.

К отзывам можно оставлять комментарии.

&nbsp;

## Технологии:

Python 3.7.14

Django 2.2.19

Docker 20.10.17

Docker Compose 3.8

PostgreSQL 13.0

nginx 1.21.3

Gunicorn 20.0.4

&nbsp;

## Как запустить проект в контейнере:

Чтобы впервые развернуть проект из контейнеров локально, находясь в директории */infra_sp2/infra/*, введите комнаду:
```
docker-compose up -d
```
Затем создайте и примените миграции в контейнере. Для этого последовательно введите команды:
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```
Чтобы заполнить базу данных контейнера данными из фикстур, введите в терминале команды для удаления объектов ContentType, а затем команду для заполнения базы данными:
```
docker-compose exec web python3 manage.py shell
>>> from django.contrib.contenttypes.models import ContentType
>>> ContentType.objects.all().delete()
>>> quit()
docker-compose exec web python manage.py loaddata fixtures.json
```
Чтобы создать суперюзера, введите команду и запрашиваемые данные:
```
docker-compose exec web python manage.py createsuperuser
```
Затем необходимо собрать статику для корректного отображения сайта в браузере:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Остановить контейнеры можно командой:
```
docker-compose stop
```
Остановленные контейнеры можно вновь запустить командой:
```
docker-compose start
```
Чтобы остановить контейнеры и удалить их со своей машины, введите:
```
docker-compose down
```
&nbsp;

## Шаблон наполнения env-файла:

```
SECRET_KEY = 'very_secret_key'
DEBUG = True/False
ALLOWED_HOSTS = ['allowed_host_1', 'allowed_host_2', ... , 'allowed_host_n']


DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db_name
DB_PORT=1234
```
&nbsp;

## API проекта YaMDb

Полная документация доступна по ссылке *http://localhost/redoc/*. Ниже приведены некоторые примеры корректных запросов к API:

&nbsp;

### Регистрация и авторизация нового пользователя:

> POST | http://127.0.0.1:8000/api/v1/auth/signup/

```
{
"email": "pochta@mylo.ru",
"username": "test_user"
}
```
> 200 OK

&nbsp;

> POST | http://127.0.0.1:8000/api/v1/auth/token/

```
{
"username": "test_user",
"confirmation_code": "61p-c0443f686f2ea7e2444f"
}
```
> 200 OK

&nbsp;

### Получение списка всех категорий:

> GET | http://127.0.0.1:8000/api/v1/categories/

> 200 OK

&nbsp;

### Поиск по жанрам:

> GET | http://127.0.0.1:8000/api/v1/genres/?search=rock-n-roll

> 200 OK

&nbsp;

### Получение списка произведений, отфильтрованных по году и категории:

> GET | http://127.0.0.1:8000/api/v1/titles/?year=1994&category=movie

> 200 OK

&nbsp;

### Добавление произведения:

> POST | http://127.0.0.1:8000/api/v1/titles/

```
{
"name": "8 1/2",
"year": 1963,
"description": "Фантазия Феллини о месте художника в современном мире.",
"genre": [
"fantasy", "drama"
],
"category": "movie"
}

```

> 201 CREATED

&nbsp;

### Полуение отзыва по id:

> GET | http://127.0.0.1:8000/api/v1/titles/1/reviews/2/

> 200 OK

&nbsp;

### Частичное обновление отзыва:

> PATCH | http://127.0.0.1:8000/api/v1/titles/1/reviews/1/

```
{
  "text": "Класс! UPD: всем советую!",
  "score": 10
}
```
> 200 OK

&nbsp;

### Удаление комментария:

> DELETE | http://127.0.0.1:8000/api/v1/titles/5/reviews/2/comments/1/

> 204 NO_CONTENT

&nbsp;

### Получение и изменение данных пользователя по username:

> GET | http://127.0.0.1:8000/api/v1/users/bingobongo/

> 200 OK

&nbsp;

> PATCH | http://127.0.0.1:8000/api/v1/users/bingobongo/

> 200 OK

&nbsp;

### Получение и изменение данный своей учетной записи:

> GET | http://127.0.0.1:8000/api/v1/users/me/

> 200 OK

&nbsp;

> PATCH | http://127.0.0.1:8000/api/v1/users/me/

> 200 OK

&nbsp;

### Авторы:

*Кирилл Павлов (тимлид), Александр Алексеев, Анастасия Антипина*