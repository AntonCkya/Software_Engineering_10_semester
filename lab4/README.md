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

## Описание БД

База данных PostgreSQL, схема описана в файле `schema.sql`.

### Таблица `users`

| Столбец | Тип | Описание |
|---|---|---|
| `id` | UUID | Первичный ключ, генерируется автоматически |
| `login` | VARCHAR(100) | Логин пользователя (уникальный, не пустой) |
| `first_name` | VARCHAR(100) | Имя |
| `last_name` | VARCHAR(100) | Фамилия |
| `email` | VARCHAR(255) | Email (уникальный, с проверкой формата) |
| `password_hash` | VARCHAR(255) | Хеш пароля |
| `created_at` | TIMESTAMPTZ | Дата создания |
| `updated_at` | TIMESTAMPTZ | Дата обновления (обновляется триггером) |

Индексы:
- `idx_users_login` — по логину
- `idx_users_email` — по email
- `idx_users_first_name_trgm` — триграммный GIN индекс по имени (для поиска по маске)
- `idx_users_last_name_trgm` — триграммный GIN индекс по фамилии (для поиска по маске)

### Таблица `parcels`

| Столбец | Тип | Описание |
|---|---|---|
| `id` | UUID | Первичный ключ, генерируется автоматически |
| `owner_id` | UUID | Внешний ключ на `users.id` (ON DELETE CASCADE) |
| `tracking_number` | VARCHAR(50) | Трек-номер (уникальный, не пустой) |
| `description` | TEXT | Описание посылки |
| `weight_kg` | NUMERIC(10, 2) | Вес в кг (>= 0) |
| `dimensions` | VARCHAR(50) | Габариты (по типу "10x20x30 см") |
| `created_at` | TIMESTAMPTZ | Дата создания |
| `updated_at` | TIMESTAMPTZ | Дата обновления (обновляется триггером) |

Индексы:
- `idx_parcels_owner_id` — по owner_id
- `idx_parcels_tracking_number` — по трек-номеру

### Таблица `deliveries`

| Столбец | Тип | Описание |
|---|---|---|
| `id` | UUID | Первичный ключ, генерируется автоматически |
| `sender_id` | UUID | Внешний ключ на `users.id` (ON DELETE RESTRICT) |
| `recipient_id` | UUID | Внешний ключ на `users.id` (ON DELETE RESTRICT) |
| `parcel_id` | UUID | Внешний ключ на `parcels.id` (ON DELETE RESTRICT) |
| `status` | VARCHAR(20) | Статус: `pending`, `in_transit`, `delivered`, `cancelled` |
| `sender_address` | TEXT | Адрес отправителя |
| `recipient_address` | TEXT | Адрес получателя |
| `estimated_delivery_date` | TIMESTAMPTZ | Планируемая дата доставки |
| `actual_delivery_date` | TIMESTAMPTZ | Фактическая дата доставки |
| `created_at` | TIMESTAMPTZ | Дата создания |
| `updated_at` | TIMESTAMPTZ | Дата обновления (обновляется триггером) |

Индексы:
- `idx_deliveries_sender_id` — по отправителю
- `idx_deliveries_recipient_id` — по получателю
- `idx_deliveries_parcel_id` — по посылке
- `idx_deliveries_status_created` — составной индекс по статусу и дате создания

### Тестовые данные

В файле `data.sql` содержатся тестовые данные

## Описание эндпоинтов

Можно найти в lab2

## Хранилище

Хранение данных осуществляется в PostgreSQL через SQLAlchemy ORM (асинхронный asyncpg драйвер).


## Создание и запуск БД

- Создание через Docker Compose:

```
docker compose up -d --build
```

Появится 2 контейнера, для запросов нужно использовать postgres.

Внутри контейнера можно запустить:

```
psql -U postgres -p 5432 -h localhost -d delivery
```

А дальше делать любые запросы с готовой БД (например те, что в `queries.sql`)

Также можно потестить работу через бэкенд (см lab2, относительно контрактов изменений не было)
