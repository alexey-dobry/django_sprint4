# API для Yatube

REST API проекта Yatube: посты, комментарии, группы и подписки. Документация в формате Redoc доступна по адресу http://127.0.0.1:8000/redoc/ после запуска проекта.

## Описание

Проект решает задачу программного доступа к данным блога Yatube: получение и публикация постов, комментариев, просмотр групп и управление подписками. Аутентификация по JWT-токенам; для неавторизованных пользователей доступно только чтение (кроме эндпоинта подписок).

**Основные возможности:**

- Публикации: список, создание, просмотр, изменение и удаление (свои — только автор).
- Комментарии к постам: те же операции с проверкой авторства.
- Группы (сообщества): только чтение списка и деталей.
- Подписки: список подписок текущего пользователя, подписка на пользователя (с поиском по параметру `search`). Нельзя подписаться на себя.
- JWT: получение, обновление и проверка токенов.

## Установка

**Требования:** Python 3.8–3.12 (рекомендуется 3.10 или 3.11). Python 3.13 не поддерживается из-за несовместимости Django 3.2 с удалённым модулем `cgi`.

1. Клонируйте репозиторий и перейдите в каталог проекта:

   ```bash
   git clone https://github.com/Romankomarov154/api-final-yatube-ad.git
   cd api-final-yatube-ad
   ```

2. Создайте и активируйте виртуальное окружение:

   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Установите зависимости:

   ```bash
   pip install -r requirements.txt
   ```

4. Перейдите в каталог с проектом Django и выполните миграции:

   ```bash
   cd yatube_api
   python manage.py migrate
   ```

5. (По желанию) создайте суперпользователя и запустите сервер:

   ```bash
   python manage.py createsuperuser
   python manage.py runserver
   ```

Документация API: http://127.0.0.1:8000/redoc/

## Примеры запросов

Базовый URL API: `http://127.0.0.1:8000/api/v1/`

### Получение JWT-токена

```bash
POST /api/v1/jwt/create/
Content-Type: application/json

{
  "username": "ваш_username",
  "password": "ваш_пароль"
}
```

В ответ придут поля `access` и `refresh`.

### Список постов (без авторизации)

```bash
GET /api/v1/posts/
```

### Создание поста (с авторизацией)

```bash
POST /api/v1/posts/
Authorization: Bearer <access_токен>
Content-Type: application/json

{
  "text": "Текст нового поста",
  "group": 1
}
```

### Список подписок текущего пользователя

```bash
GET /api/v1/follow/
Authorization: Bearer <access_токен>
```

С поиском по username:

```bash
GET /api/v1/follow/?search=username
Authorization: Bearer <access_токен>
```

### Подписаться на пользователя

```bash
POST /api/v1/follow/
Authorization: Bearer <access_токен>
Content-Type: application/json

{
  "following": "username_пользователя"
}
```

Коллекция запросов для Postman лежит в каталоге `postman_collection/`.
