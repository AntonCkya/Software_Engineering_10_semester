# MeowMeowExpress

MeowMeowExpress - сервис доставки посылок на Python FastAPI с MongoDB.

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

База данных MongoDB, схема описана в файле `schema_design.md`.

### Коллекция `users`

Хранит информацию о пользователях:
- `login` - логин пользователя (уникальный)
- `first_name` - имя
- `last_name` - фамилия
- `email` - email (уникальный)
- `password_hash` - хеш пароля
- `created_at` - дата создания
- `updated_at` - дата обновления

### Коллекция `parcels`

Хранит информацию о посылках:
- `owner_id` - ссылка на пользователя ( UUID4 )
- `tracking_number` - трек-номер (уникальный)
- `description` - описание посылки
- `weight_kg` - вес в кг (>= 0)
- `dimensions` - габариты (например, "10x20x30 см")
- `created_at` - дата создания
- `updated_at` - дата обновления

### Коллекция `deliveries`

Хранит информацию о доставках:
- `sender_id` - ссылка на отправителя ( UUID4 )
- `recipient_id` - ссылка на получателя ( UUID4 )
- `parcel_id` - ссылка на посылку ( UUID4 )
- `status` - статус: `pending`, `in_transit`, `delivered`, `cancelled`
- `sender_address` - адрес отправителя
- `recipient_address` - адрес получателя
- `estimated_delivery_date` - планируемая дата доставки
- `actual_delivery_date` - фактическая дата доставки
- `created_at` - дата создания
- `updated_at` - дата обновления

## Создание и запуск БД

### Запуск через Docker Compose

```bash
docker compose up -d --build
```

Появится 2 контейнера:
- `mongo_db` - MongoDB база данных
- `app` - FastAPI приложение

### Проверка статуса контейнеров

```bash
docker ps
```

### Подключение к MongoDB через shell

```bash
docker exec -it mongo_db mongosh -u root -p password
```

### Инициализация базы данных

При первом запуске Docker Compose автоматически выполнит скрипт `mongo-init.js` для создания коллекций и тестовых данных.

## Запуск приложения

### Через Docker Compose

После запуска `docker compose up -d`, приложение будет доступно по адресу:
```
http://localhost:8000
```

## API Эндпоинты

Документация доступна по адресу `/docs` (Swagger UI) или `/redoc` (ReDoc).

### Эндпоинты пользователей
- `POST /api/v1/users` - Создание нового пользователя
- `GET /api/v1/users/login/{login}` - Поиск пользователя по логину
- `POST /api/v1/users/search` - Поиск пользователей по маске имени и фамилии
- `GET /api/v1/users/me` - Получение информации о текущем пользователе

### Эндпоинты посылок
- `POST /api/v1/parcels` - Создание новой посылки
- `GET /api/v1/parcels/{parcel_id}` - Получение посылки по ID
- `GET /api/v1/parcels/user/{user_id}` - Получение всех посылок пользователя
- `GET /api/v1/parcels/tracking/{tracking_number}` - Поиск посылки по трек-номеру

### Эндпоинты доставок
- `POST /api/v1/deliveries` - Создание новой доставки
- `GET /api/v1/deliveries/{delivery_id}` - Получение доставки по ID
- `GET /api/v1/deliveries/sender/{sender_id}` - Получение доставок отправителя
- `GET /api/v1/deliveries/recipient/{recipient_id}` - Получение доставок получателя

## Тестовые данные

После запуска базы данных создаются следующие пользователи (12 штук):

| Логин | Имя | Фамилия |
|-------|-----|---------|
| ivanov_ivan | Иван | Иванов |
| petrova_anna | Анна | Петрова |
| sidorov_alex | Александр | Сидоров |
| kuznetsova_maria | Мария | Кузнецова |
| popov_dmitry | Дмитрий | Попов |
| volkova_elena | Елена | Волкова |
| novikov_sergey | Сергей | Новиков |
| morozova_olga | Ольга | Морозова |
| lebedev_andrey | Андрей | Лебедев |
| kozlova_natalia | Наталья | Козлова |
| smirnov_pavel | Павел | Смирнов |
| vasileva_irina | Ирина | Васильева |

Также создаются 12 посылок и 12 доставок с различными статусами.

## Запуск скриптов MongoDB

### Выполнение скрипта инициализации

Делать только на пустой монге, при запуске компоузом оно и так выполнится

```bash
docker exec -i mongo_db mongosh -u root -p password < mongo-init.js
```

### Выполнение скрипта валидации

```bash
docker exec -i mongo_db mongosh -u root -p password < validation.js
```

### Выполнение MongoDB команд

```bash
docker exec -i mongo_db mongosh -u root -p password < queries.js
```

### Перезапуск контейнеров (если надо)

```bash
docker-compose down -v && docker-compose up -d --build
```
