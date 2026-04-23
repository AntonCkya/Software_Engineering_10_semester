# Оптимизация запросов

## 1. Описание индексов

### Таблица `users`

| Индекс | Колонка | Тип | Назначение |
|--------|---------|-----|------------|
| `users_pkey` | `id` | B-tree (PK) | Автоматический первичный ключ. |
| `idx_users_login` | `login` | B-tree | Поиск пользователя по логину. |
| `idx_users_email` | `email` | B-tree | Поиск по email для аутентификации и валидации. |
| `idx_users_first_name_trgm` | `first_name` | GIN | Поиск по маске имени. GIN чтобы работало с триграмами. |
| `idx_users_last_name_trgm` | `last_name` | GIN | Поиск по маске фамилии. Аналогично имени. |

### Таблица `parcels`

| Индекс | Колонка | Тип | Назначение |
|--------|---------|-----|------------|
| `parcels_pkey` | `id` | B-tree (PK) | Первичный ключ. |
| `idx_parcels_owner_id` | `owner_id` | B-tree | Получение всех посылок пользователя. |
| `idx_parcels_tracking_number` | `tracking_number` | B-tree | Поиск посылки по трек-номеру. |

### Таблица `deliveries`

| Индекс | Колонка | Тип | Назначение |
|--------|---------|-----|------------|
| `deliveries_pkey` | `id` | B-tree (PK) | Первичный ключ. |
| `idx_deliveries_sender_id` | `sender_id` | B-tree | Получение доставок по отправителю. |
| `idx_deliveries_recipient_id` | `recipient_id` | B-tree | Получение доставок по получателю. |
| `idx_deliveries_parcel_id` | `parcel_id` | B-tree | JOIN с таблицей parcels. |
| `idx_deliveries_status_created` | `status, created_at DESC` | B-tree | Фильтрация по статусу с сортировкой по дате. |

---

## 2. Анализ планов выполнения (EXPLAIN ANALYZE)

### 2.1 Поиск пользователя по логину

**Запрос:**
```sql
EXPLAIN ANALYZE
SELECT id, login, first_name, last_name, email, created_at, updated_at
FROM users
WHERE login = 'ivanov_ivan';
```

**До оптимизации (без индекса):**
```
Seq Scan on users  (cost=0.00..1.15 rows=1 width=108) (actual time=0.015..0.016 rows=1 loops=1)
  Filter: (login = 'ivanov_ivan'::text)
  Rows Removed by Filter: 11
Planning Time: 0.050 ms
Execution Time: 0.025 ms
```

**После оптимизации (с индексом `idx_users_login`):**
```
Index Scan using idx_users_login on users  (cost=0.14..8.16 rows=1 width=108) (actual time=0.012..0.013 rows=1 loops=1)
  Index Cond: (login = 'ivanov_ivan'::text)
Planning Time: 0.080 ms
Execution Time: 0.020 ms
```

**Вывод:** На мелких данных особо не видно, но чем больше таблица тем сильнее разница (логарифм вместо линии).

---

### 2.2 Поиск пользователя по маске имени

**Запрос:**
```sql
EXPLAIN ANALYZE
SELECT id, login, first_name, last_name, email, created_at, updated_at
FROM users
WHERE first_name ILIKE '%Ан%';
```

**До оптимизации (без trigram индекса):**
```
Seq Scan on users  (cost=0.00..1.15 rows=1 width=108) (actual time=0.020..0.025 rows=3 loops=1)
  Filter: (first_name ~~* '%Ан%'::text)
  Rows Removed by Filter: 9
Planning Time: 0.045 ms
Execution Time: 0.035 ms
```

**После оптимизации (с GIN trigram индексом):**
```
Bitmap Heap Scan on users  (cost=8.03..12.50 rows=3 width=108) (actual time=0.018..0.020 rows=3 loops=1)
  Recheck Cond: (first_name ~~* '%Ан%'::text)
  Heap Blocks: exact=2
  ->  Bitmap Index Scan on idx_users_first_name_trgm  (cost=0.00..8.03 rows=3 width=0) (actual time=0.012..0.012 rows=3 loops=1)
        Index Cond: (first_name ~~* '%Ан%'::text)
Planning Time: 0.100 ms
Execution Time: 0.030 ms
```

**Вывод:** B-tree не работает с масками, для этого нужно использовать GIN на основе триграм.

---

## 3. Стратегия партиционирования

### Таблица `deliveries` — партиционирование по дате

Сделано чисто как мыслительный эксперимент, как можно партицировать данные. Партиционирование по `created_at`:

```sql
CREATE TABLE deliveries_2025_01 PARTITION OF deliveries
    FOR VALUES FROM ('2025-01-01') TO ('2025-02-01');
CREATE TABLE deliveries_2025_02 PARTITION OF deliveries
    FOR VALUES FROM ('2025-02-01') TO ('2025-03-01');
```

**Преимущества:**
- Запросы с фильтром по дате ходят только в нужные партиции.
- Архивирование (миграция в холодные хранилища) данных целыми партициями.
- Параллельное выполнение запросов по разным партициям.

**Недостатки:**
- Усложнение схемы.
- Сейчас нет автоматики по созданию партиций.
