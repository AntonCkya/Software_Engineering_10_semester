# Проектирование документной модели MongoDB

## Обзор

Проектируемая база данных для сервиса доставки посылок **MeowMeowExpress** на основе MongoDB будет содержать три коллекции:

1. **users** — информация о пользователях
2. **parcels** — информация о посылках
3. **deliveries** — информация о доставках

## Коллекция `users`

### Структура документа:
```javascript
{
  _id: ObjectId("..."),
  login: String,
  first_name: String,
  last_name: String,
  email: String,
  password_hash: String,
  created_at: ISODate,
  updated_at: ISODate
}
```

### Поля:
| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `_id` | ObjectId | Да | Уникальный идентификатор (автоматически генерируется) |
| `login` | String | Да | Логин пользователя, уникальный |
| `first_name` | String | Да | Имя пользователя |
| `last_name` | String | Да | Фамилия пользователя |
| `email` | String | Да | Email, уникальный |
| `password_hash` | String | Да | Хеш пароля |
| `created_at` | Date | Да | Дата создания пользователя |
| `updated_at` | Date | Да | Дата последнего обновления |

### Индексы:
- `_id` (PK, автоматически)
- `login` (unique)
- `email` (unique)
- `first_name` (text index для поиска по маске)
- `last_name` (text index для поиска по маске)

### Обоснование выбора структуры:
- Все поля хранятся напрямую в документе — нет необходимости в нормализации
- Email и login уникальны — создаём unique индексы
- Для поиска по маске используем text index на `first_name` и `last_name`

---

## Коллекция `parcels`

### Структура документа:
```javascript
{
  _id: ObjectId("..."),
  owner_id: ObjectId,
  tracking_number: String,
  description: String,
  weight_kg: Number,
  dimensions: String,
  created_at: ISODate,
  updated_at: ISODate
}
```

### Поля:
| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `_id` | ObjectId | Да | Уникальный идентификатор |
| `owner_id` | ObjectId | Да | Ссылка на пользователя (внешний ключ на users._id) |
| `tracking_number` | String | Да | Уникальный трек-номер |
| `description` | String | Да | Описание посылки |
| `weight_kg` | Number | Да | Вес в килограммах (>= 0) |
| `dimensions` | String | Да | Габариты (например, "10x20x30 см") |
| `created_at` | Date | Да | Дата создания |
| `updated_at` | Date | Да | Дата последнего обновления |

### Индексы:
- `_id` (PK)
- `owner_id` (для поиска посылок пользователя)
- `tracking_number` (unique)

### Обоснование выбора между embedded/references:
- **owner_id** — используем **reference** (ObjectId), так как:
  - Пользователь может иметь множество посылок (много к одному)
  - При удалении пользователя посылки должны быть удалены (CASCADE) — это легко реализуется через application-level логику в MongoDB
  - Ссылка на пользователя не меняется часто
  - При необходимости получить информацию о владельце делаем отдельный запрос (или use `$lookup` в агрегации)

---

## Коллекция `deliveries`

### Структура документа:
```javascript
{
  _id: ObjectId("..."),
  sender_id: ObjectId,
  recipient_id: ObjectId,
  parcel_id: ObjectId,
  status: String,
  sender_address: String,
  recipient_address: String,
  estimated_delivery_date: ISODate,
  actual_delivery_date: ISODate,
  created_at: ISODate,
  updated_at: ISODate
}
```

### Поля:
| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `_id` | ObjectId | Да | Уникальный идентификатор |
| `sender_id` | ObjectId | Да | Ссылка на отправителя (users._id) |
| `recipient_id` | ObjectId | Да | Ссылка на получателя (users._id) |
| `parcel_id` | ObjectId | Да | Ссылка на посылку (parcels._id) |
| `status` | String | Да | Статус доставки: 'pending', 'in_transit', 'delivered', 'cancelled' |
| `sender_address` | String | Да | Адрес отправителя |
| `recipient_address` | String | Да | Адрес получателя |
| `estimated_delivery_date` | Date | Нет | Планируемая дата доставки |
| `actual_delivery_date` | Date | Нет | Фактическая дата доставки |
| `created_at` | Date | Да | Дата создания |
| `updated_at` | Date | Да | Дата последнего обновления |

### Индексы:
- `_id` (PK)
- `sender_id` (для поиска доставок отправителя)
- `recipient_id` (для поиска доставок получателя)
- `parcel_id` (для поиска по посылке)
- `status` + `created_at` (составной для сортировки по статусу)

### Обоснование выбора между embedded/references:
- **sender_id, recipient_id, parcel_id** — используем **references** (ObjectId), так как:
  - Один пользователь может быть отправителем или получателем множества доставок
  - Одна посылка может участвовать в нескольких доставках (хотя в логике приложения это ограничено)
  - Ссылки не меняются часто
  - В MongoDB нет FOREIGN KEY CONSTRAINT, поэтому ссылки на несуществующие документы возможны — это обрабатывается на уровне приложения

---

## Сравнение: PostgreSQL vs MongoDB

| Аспект | PostgreSQL (ЛР3) | MongoDB (ЛР4) |
|--------|------------------|---------------|
| Тип БД | Реляционная | Документная |
| Ключи | UUID (string) | ObjectId |
| Внешние ключи | Синтаксис SQL (FOREIGN KEY) | Reference (ObjectId) + application logic |
| Связи | JOIN таблицы | Ссылки + $lookup в агрегации |
| Валидация | CHECK CONSTRAINT | $jsonSchema |
| Индексы | B-tree, GIN (trigram) | B-tree, Text index |
| Структура | Строгая схема | Схема-опционально (flexible) |

---

## Принципы проектирования

1. **Нормализация vs Денормализация**:
   - Основная модель нормализована (разделение на 3 коллекции)
   - Минимальная денормализация: только ссылки, без дублирования данных

2. **Связи "один ко многим"**:
   - `users` → `parcels`: один пользователь владеет многими посылками
   - `users` → `deliveries` (как sender/recipient): один пользователь может участвовать в множестве доставок

3. **Каскадное удаление**:
   - В PostgreSQL реализовано через `ON DELETE CASCADE`
   - В MongoDB реализуется на уровне приложения: при удалении пользователя сначала удаляются его посылки и доставки

4. **Текстовый поиск**:
   - В PostgreSQL: `pg_trgm` + `GIN` индекс + `ILIKE '%mask%'`
   - В MongoDB: Text index + `$text` query

---

## Примеры связей

### Связь User → Parcels (один ко многим)
```javascript
// Пользователь
{
  _id: ObjectId("..."),
  login: "ivanov_ivan",
  first_name: "Иван",
  last_name: "Иванов",
  ...
}

// Посылки пользователя (ссылка на пользователя)
{
  _id: ObjectId("..."),
  owner_id: ObjectId("id_ivanov"), // ссылка на пользователя
  tracking_number: "TRK001A2B3C4D",
  ...
}
```

### Связь User → Deliveries (один ко многим, как sender/recipient)
```javascript
// Доставка (ссылки на отправителя, получателя и посылку)
{
  _id: ObjectId("..."),
  sender_id: ObjectId("id_ivanov"),
  recipient_id: ObjectId("id_petrova"),
  parcel_id: ObjectId("id_parcel_1"),
  status: "delivered",
  ...
}
```

---

## Выводы

Выбрана архитектура с тремя отдельными коллекциями, связанными через ObjectId references. Такой подход:

- Сохраняет гибкость MongoDB
- Позволяет легко масштабировать каждую коллекцию
- Упрощает добавление новых полей без изменения схемы
- Требует дополнительной логики для обеспечения целостности данных (вместо внешних ключей)
- Позволяет использовать текстовый поиск для удобного поиска пользователей по маске

Для поддержания целостности данных в приложении реализованы:
1. Валидация ObjectId перед созданием ссылок
2. Каскадное удаление на уровне приложения
3. Проверка существования ссылаемых документов перед созданием записей
