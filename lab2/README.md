# MeowMeowExpress

MeowMeowExpress - сервис доставки посылок на Python FastAPI.

## Описание задания

Вариант №6: Сервис доставки https://www.cdek.ru/ru/

Приложение должно содержать следующие данные:
- Пользователь
- Посылка
- Доставка
Реализовать API:
- Создание нового пользователя
- Поиск пользователя по логину
- Поиск пользователя по маске имя и фамилии
- Создание посылки
- Получение посылок пользователя
- Создание доставки от пользователя к пользователю
- Получение информации о доставке по получателю
- Получение информации о доставке по отправителю

## Описание эндпоинтов

- GET `/`

Корневая ручка с описанием сервиса

Ответ:
```
{
  "name": "MeowMeowExpress",
  "version": "0.0.1",
  "environment": "dev",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

- GET `/health`

Healthcheck ручка

Ответ:
```
{
  "status": "healthy",
  "environment": "dev",
  "version": "0.0.1"
}
```

- POST `/api/v1/auth/register`

Ручка для регистрации пользователей

Формат входных данных:
```
{
  "login": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "password": "string"
}
```
Ответ:
```
{
  "id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
  "login": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "created_at": "2026-03-22T21:32:00.339000",
  "updated_at": "2026-03-22T21:32:00.339034"
}
```

- POST `/api/v1/auth/login`

Ручка для входа пользователя (получения access и refresh токенов)

Формат входных данных:
```
{
  "login": "string",
  "password": "string"
}
```
Ответ:
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MjlmYzBiNC05ZjU4LTQ2YWItYjQ4Yi00YWI3OTZjNjQ4M2IiLCJsb2dpbiI6InN0cmluZyIsImV4cCI6MTc3NDIxNzAwMiwidHlwZSI6ImFjY2VzcyJ9.EvA0qtPHLdNbRV3DDOT6OXenLBLH2BwrZRFDtyi513A",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MjlmYzBiNC05ZjU4LTQ2YWItYjQ4Yi00YWI3OTZjNjQ4M2IiLCJsb2dpbiI6InN0cmluZyIsImV4cCI6MTc3NDgyMDAwMiwidHlwZSI6InJlZnJlc2gifQ.HmCZqEdaz9ZdW5muZBnKiwZj5AhSGvz6TcXqX6w4l6k",
  "token_type": "bearer"
}
```

- POST `/api/v1/auth/refresh`

По refresh токену возвращает новые access и refresh токены

Формат входных данных:
```
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MjlmYzBiNC05ZjU4LTQ2YWItYjQ4Yi00YWI3OTZjNjQ4M2IiLCJsb2dpbiI6InN0cmluZyIsImV4cCI6MTc3NDgyMDAwMiwidHlwZSI6InJlZnJlc2gifQ.HmCZqEdaz9ZdW5muZBnKiwZj5AhSGvz6TcXqX6w4l6k"
}
```
Ответ:
```
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MjlmYzBiNC05ZjU4LTQ2YWItYjQ4Yi00YWI3OTZjNjQ4M2IiLCJsb2dpbiI6InN0cmluZyIsImV4cCI6MTc3NDIxNzExOSwidHlwZSI6ImFjY2VzcyJ9.lopK5B6kBIpgJoQ9h3Z2_eFP-VwUQKhYpPsckKhZ_yo",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MjlmYzBiNC05ZjU4LTQ2YWItYjQ4Yi00YWI3OTZjNjQ4M2IiLCJsb2dpbiI6InN0cmluZyIsImV4cCI6MTc3NDgyMDExOSwidHlwZSI6InJlZnJlc2gifQ.O1O4qgdnwSbwhaOk6fcFO68H54XjbYieqlUcghvFCeQ",
  "token_type": "bearer"
}
```

- GET `/api/v1/users/login/{login}`

Ручка для поиска юзера по логину

Формат входных данных:
```
login: в path
```
Ответ:
```
{
  "id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
  "login": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "created_at": "2026-03-22T21:32:00.339000",
  "updated_at": "2026-03-22T21:32:00.339034"
}
```

- POST `/api/v1/users/search`

Ручка для поиска юзеров по маске first_name или last_name

Можно ввести обе маски или одну.

(POST метод из-за body)

Формат входных данных:
```
{
  "first_name_mask": "str*",
  "last_name_mask": "string"
}
```
Ответ:
```
{
  "users": [
    {
      "id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
      "login": "string",
      "first_name": "string",
      "last_name": "string",
      "email": "user@example.com",
      "created_at": "2026-03-22T21:32:00.339000",
      "updated_at": "2026-03-22T21:32:00.339034"
    }
  ],
  "total": 1
}
```

- GET `/api/v1/users/me`

Ручка для получения информации о залогиненом пользователе (из токена в хедере)

Формат входных данных:
```
-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3MjlmYzBiNC05ZjU4LTQ2YWItYjQ4Yi00YWI3OTZjNjQ4M2IiLCJsb2dpbiI6InN0cmluZyIsImV4cCI6MTc3NDIxNzAwMiwidHlwZSI6ImFjY2VzcyJ9.EvA0qtPHLdNbRV3DDOT6OXenLBLH2BwrZRFDtyi513A'
```
Ответ:
```
{
  "id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
  "login": "string",
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "created_at": "2026-03-22T21:32:00.339000",
  "updated_at": "2026-03-22T21:32:00.339034"
}
```

- POST `/api/v1/parcels`

Ручка для создания посылок

Защищена токеном

Формат входных данных:
```
{
  "owner_id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
  "description": "string",
  "weight_kg": 1,
  "dimensions": "10х20х30"
}
```
Ответ:
```
{
  "id": "73b2719a-f1ed-4bfc-a272-e57ab8aedb13",
  "owner_id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
  "tracking_number": "TRKC3DF088E995A",
  "description": "string",
  "weight_kg": 1,
  "dimensions": "10х20х30",
  "created_at": "2026-03-22T21:39:37.263870",
  "updated_at": "2026-03-22T21:39:37.263877"
}
```

- GET `/api/v1/parcels/{parcel_id}`

Ручка для получения посылки по ее parcel_id

Защищена токеном

Формат входных данных:
```
parcel_id: в path
```
Ответ:
```
{
  "id": "73b2719a-f1ed-4bfc-a272-e57ab8aedb13",
  "owner_id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
  "tracking_number": "TRKC3DF088E995A",
  "description": "string",
  "weight_kg": 1,
  "dimensions": "10х20х30",
  "created_at": "2026-03-22T21:39:37.263870",
  "updated_at": "2026-03-22T21:39:37.263877"
}
```

- GET `/api/v1/parcels/user/{user_id}`

Ручка для получения посылок по user_id (посылки, где user_id является owner_id)

Защищена токеном

Формат входных данных:
```
user_id: в path
```
Ответ:
```
{
  "parcels": [
    {
      "id": "73b2719a-f1ed-4bfc-a272-e57ab8aedb13",
      "owner_id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
      "tracking_number": "TRKC3DF088E995A",
      "description": "string",
      "weight_kg": 1,
      "dimensions": "10х20х30",
      "created_at": "2026-03-22T21:39:37.263870",
      "updated_at": "2026-03-22T21:39:37.263877"
    }
  ],
  "total": 1
}
```

- GET `/api/v1/parcels/tracking/{tracking_number}`

Получить посылку по трек-номеру

Защищена токеном

Формат входных данных:
```
tracking_number: в path
```
Ответ:
```
{
  "id": "73b2719a-f1ed-4bfc-a272-e57ab8aedb13",
  "owner_id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
  "tracking_number": "TRKC3DF088E995A",
  "description": "string",
  "weight_kg": 1,
  "dimensions": "10х20х30",
  "created_at": "2026-03-22T21:39:37.263870",
  "updated_at": "2026-03-22T21:39:37.263877"
}
```

- POST `/api/v1/deliveries`

Создание доставки

Защищена токеном

Формат входных данных:
```
{
  "sender_id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
  "recipient_id": "a55ef479-4605-4a54-9435-2bde8359a43c",
  "parcel_id": "73b2719a-f1ed-4bfc-a272-e57ab8aedb13",
  "sender_address": "string 1",
  "recipient_address": "string 2",
  "estimated_delivery_date": "2026-03-22T18:45:59.044Z"
}
```
Ответ:
```
{
  "id": "98c63a66-aa1a-42fd-ac41-99adf69c6551",
  "sender_id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
  "recipient_id": "a55ef479-4605-4a54-9435-2bde8359a43c",
  "parcel_id": "73b2719a-f1ed-4bfc-a272-e57ab8aedb13",
  "status": "pending",
  "sender_address": "string 1",
  "recipient_address": "string 2",
  "estimated_delivery_date": "2026-03-22T18:45:59.044000Z",
  "actual_delivery_date": null,
  "created_at": "2026-03-22T21:46:55.623126",
  "updated_at": "2026-03-22T21:46:55.623137"
}
```

- GET `/api/v1/deliveries/{delivery_id}`

Получение объекта доставки

Защищена токеном

Формат входных данных:
```
delivery_id: в path
```
Ответ:
```
{
  "id": "98c63a66-aa1a-42fd-ac41-99adf69c6551",
  "sender_id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
  "recipient_id": "a55ef479-4605-4a54-9435-2bde8359a43c",
  "parcel_id": "73b2719a-f1ed-4bfc-a272-e57ab8aedb13",
  "status": "pending",
  "sender_address": "string 1",
  "recipient_address": "string 2",
  "estimated_delivery_date": "2026-03-22T18:45:59.044000Z",
  "actual_delivery_date": null,
  "created_at": "2026-03-22T21:46:55.623126",
  "updated_at": "2026-03-22T21:46:55.623137"
}
```

- GET `/api/v1/deliveries/sender/{sender_id}`

Получить все доставки по id отправителя

Защищена токеном

Формат входных данных:
```
sender_id: в path
```
Ответ:
```
{
  "deliveries": [
    {
      "id": "98c63a66-aa1a-42fd-ac41-99adf69c6551",
      "sender_id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
      "recipient_id": "a55ef479-4605-4a54-9435-2bde8359a43c",
      "parcel_id": "73b2719a-f1ed-4bfc-a272-e57ab8aedb13",
      "status": "pending",
      "sender_address": "string 1",
      "recipient_address": "string 2",
      "estimated_delivery_date": "2026-03-22T18:45:59.044000Z",
      "actual_delivery_date": null,
      "created_at": "2026-03-22T21:46:55.623126",
      "updated_at": "2026-03-22T21:46:55.623137"
    }
  ],
  "total": 1
}
```

- GET `/api/v1/deliveries/recipient/{recipient_id}`

Получить все доставки по id получателя

Защищена токеном

Формат входных данных:
```
recipient_id: в path
```
Ответ:
```
{
  "deliveries": [
    {
      "id": "98c63a66-aa1a-42fd-ac41-99adf69c6551",
      "sender_id": "729fc0b4-9f58-46ab-b48b-4ab796c6483b",
      "recipient_id": "a55ef479-4605-4a54-9435-2bde8359a43c",
      "parcel_id": "73b2719a-f1ed-4bfc-a272-e57ab8aedb13",
      "status": "pending",
      "sender_address": "string 1",
      "recipient_address": "string 2",
      "estimated_delivery_date": "2026-03-22T18:45:59.044000Z",
      "actual_delivery_date": null,
      "created_at": "2026-03-22T21:46:55.623126",
      "updated_at": "2026-03-22T21:46:55.623137"
    }
  ],
  "total": 1
}
```

## Аутентификация

Аутентификация осуществляется парой access и refresh JWT токенов.

Пользователь аутентифицируется короткоживущим access токеном в хедере: `-H 'Authorization: Bearer {TOKEN}`

Для обновления токена можно выполнить `/login`, или обновиться с помощью долгоживущего refresh токена `/refresh` (refresh токен также обновится)

## Хранилище

Хранение данных во 2 лабораторной осуществляется in-memory, с учетом переезда на реляционную БД (in-memory хранилище наследуется от абстрактного класса, который используется в роутерах)

## Документация

Документацию можно найти в файле `openapi.yaml`. Также при запуске приложения собирается документация на ручках `/docs` (swagger) и `/redoc` (redoc)

## Сборка

- Если запускаем без docker:

(требуется установленный python)

1) Установка зависимостей

```
pip install -r requirements.txt
```

Если есть проблемы с доступом к pypi можно прокинуть зеркало

```
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
(или любое другое)

2) Запуск

```
python3 main.py
```

- Если запускаем через docker:

```
docker-compose up -d --build
```

или 

```
docker compose up -d --build
```

Если есть проблемы с доступом к pypi можно также прокинуть зеркало в Dockerfile, добавив к pip install `-i https://pypi.tuna.tsinghua.edu.cn/simple`

## Тестирование

Для тестирования можно использовать Swagger UI по ручке `/docs`. Также подготовлены тесты ручек:

```
pytest -v
```

Можно запустить тесты в контейнере:

```
docker-compose -f docker-compose.test.yaml up --build
```

## Линтеры

```
ruff check
```

All checks passed!
