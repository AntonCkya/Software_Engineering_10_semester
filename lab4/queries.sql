-- 1. Создание нового пользователя
INSERT INTO users (login, first_name, last_name, email, password_hash)
VALUES (
    'new_user_login',
    'Имя',
    'Фамилия',
    'newuser@example.com',
    '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'
)
RETURNING id, login, first_name, last_name, email, created_at, updated_at;


-- 2. Поиск пользователя по логину
SELECT id, login, first_name, last_name, email, created_at, updated_at
FROM users
WHERE login = 'ivanov_ivan';


-- 3. Поиск пользователя по маске имени и фамилии
SELECT id, login, first_name, last_name, email, created_at, updated_at
FROM users
WHERE first_name ILIKE '%Ан%'
  AND last_name ILIKE '%ов%';


-- 4. Создание посылки
INSERT INTO parcels (owner_id, tracking_number, description, weight_kg, dimensions)
VALUES (
    (SELECT id FROM users WHERE login = 'ivanov_ivan'),
    'TRKNEW123456',
    'Новая посылка',
    2.50,
    '40x30x20 см'
)
RETURNING id, owner_id, tracking_number, description, weight_kg, dimensions, created_at, updated_at;


-- 5. Получение посылок пользователя
SELECT id, owner_id, tracking_number, description, weight_kg, dimensions, created_at, updated_at
FROM parcels
WHERE owner_id = (SELECT id FROM users WHERE login = 'ivanov_ivan')
ORDER BY created_at DESC;


-- 6. Создание доставки от пользователя к пользователю
INSERT INTO deliveries (
    sender_id,
    recipient_id,
    parcel_id,
    status,
    sender_address,
    recipient_address,
    estimated_delivery_date
)
VALUES (
    (SELECT id FROM users WHERE login = 'ivanov_ivan'),
    (SELECT id FROM users WHERE login = 'petrova_anna'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRKNEW123456'),
    'pending',
    'г. Москва, ул. Ленина, д. 1',
    'г. Санкт-Петербург, ул. Невский пр., д. 10',
    NOW() + INTERVAL '5 days'
)
RETURNING id, sender_id, recipient_id, parcel_id, status,
          sender_address, recipient_address,
          estimated_delivery_date, actual_delivery_date,
          created_at, updated_at;


-- 7. Получение информации о доставке по получателю
SELECT
    d.id,
    d.sender_id,
    d.recipient_id,
    d.parcel_id,
    d.status,
    d.sender_address,
    d.recipient_address,
    d.estimated_delivery_date,
    d.actual_delivery_date,
    d.created_at,
    d.updated_at,
    s.login AS sender_login,
    s.first_name AS sender_first_name,
    s.last_name AS sender_last_name,
    r.login AS recipient_login,
    r.first_name AS recipient_first_name,
    r.last_name AS recipient_last_name,
    p.tracking_number,
    p.description AS parcel_description
FROM deliveries d
JOIN users s ON d.sender_id = s.id
JOIN users r ON d.recipient_id = r.id
JOIN parcels p ON d.parcel_id = p.id
WHERE d.recipient_id = (SELECT id FROM users WHERE login = 'petrova_anna')
ORDER BY d.created_at DESC;


-- 8. Получение информации о доставке по отправителю
SELECT
    d.id,
    d.sender_id,
    d.recipient_id,
    d.parcel_id,
    d.status,
    d.sender_address,
    d.recipient_address,
    d.estimated_delivery_date,
    d.actual_delivery_date,
    d.created_at,
    d.updated_at,
    s.login AS sender_login,
    s.first_name AS sender_first_name,
    s.last_name AS sender_last_name,
    r.login AS recipient_login,
    r.first_name AS recipient_first_name,
    r.last_name AS recipient_last_name,
    p.tracking_number,
    p.description AS parcel_description
FROM deliveries d
JOIN users s ON d.sender_id = s.id
JOIN users r ON d.recipient_id = r.id
JOIN parcels p ON d.parcel_id = p.id
WHERE d.sender_id = (SELECT id FROM users WHERE login = 'ivanov_ivan')
ORDER BY d.created_at DESC;
