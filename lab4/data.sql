INSERT INTO users (login, first_name, last_name, email, password_hash) VALUES
('ivanov_ivan', 'Иван', 'Иванов', 'ivanov@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('petrova_anna', 'Анна', 'Петрова', 'petrova@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('sidorov_alex', 'Александр', 'Сидоров', 'sidorov@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('kuznetsova_maria', 'Мария', 'Кузнецова', 'kuznetsova@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('popov_dmitry', 'Дмитрий', 'Попов', 'popov@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('volkova_elena', 'Елена', 'Волкова', 'volkova@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('novikov_sergey', 'Сергей', 'Новиков', 'novikov@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('morozova_olga', 'Ольга', 'Морозова', 'morozova@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('lebedev_andrey', 'Андрей', 'Лебедев', 'lebedev@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('kozlova_natalia', 'Наталья', 'Козлова', 'kozlova@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('smirnov_pavel', 'Павел', 'Смирнов', 'smirnov@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ'),
('vasileva_irina', 'Ирина', 'Васильева', 'vasileva@example.com', '$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ');


INSERT INTO parcels (owner_id, tracking_number, description, weight_kg, dimensions) VALUES
((SELECT id FROM users WHERE login = 'ivanov_ivan'),    'TRK001A2B3C4D', 'Документы', 0.50, '30x20x5 см'),
((SELECT id FROM users WHERE login = 'ivanov_ivan'),    'TRK002E5F6G7H', 'Книги', 3.20, '40x30x15 см'),
((SELECT id FROM users WHERE login = 'petrova_anna'),   'TRK003I8J9K0L', 'Одежда', 1.50, '50x40x10 см'),
((SELECT id FROM users WHERE login = 'sidorov_alex'),   'TRK004M1N2O3P', 'Электроника', 2.00, '35x25x10 см'),
((SELECT id FROM users WHERE login = 'kuznetsova_maria'),'TRK005Q4R5S6T', 'Косметика', 0.80, '25x20x8 см'),
((SELECT id FROM users WHERE login = 'popov_dmitry'),   'TRK006U7V8W9X', 'Игрушки', 1.20, '45x35x20 см'),
((SELECT id FROM users WHERE login = 'volkova_elena'),  'TRK007Y0Z1A2B', 'Обувь', 1.00, '35x25x12 см'),
((SELECT id FROM users WHERE login = 'novikov_sergey'), 'TRK008C3D4E5F', 'Спорттовары', 5.00, '60x40x30 см'),
((SELECT id FROM users WHERE login = 'morozova_olga'),  'TRK009G6H7I8J', 'Посуда', 2.50, '40x30x25 см'),
((SELECT id FROM users WHERE login = 'lebedev_andrey'), 'TRK010K9L0M1N', 'Аксессуары', 0.30, '20x15x5 см'),
((SELECT id FROM users WHERE login = 'kozlova_natalia'),'TRK011O2P3Q4R', 'Подарки', 1.80, '35x25x15 см'),
((SELECT id FROM users WHERE login = 'smirnov_pavel'),  'TRK012S5T6U7V', 'Канцтовары', 0.70, '30x20x10 см');


INSERT INTO deliveries (sender_id, recipient_id, parcel_id, status, sender_address, recipient_address, estimated_delivery_date) VALUES
(
    (SELECT id FROM users WHERE login = 'ivanov_ivan'),
    (SELECT id FROM users WHERE login = 'petrova_anna'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK001A2B3C4D'),
    'delivered',
    'г. Москва, ул. Ленина, д. 1',
    'г. Санкт-Петербург, ул. Невский пр., д. 10',
    NOW() - INTERVAL '5 days'
),
(
    (SELECT id FROM users WHERE login = 'ivanov_ivan'),
    (SELECT id FROM users WHERE login = 'sidorov_alex'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK002E5F6G7H'),
    'in_transit',
    'г. Москва, ул. Ленина, д. 1',
    'г. Казань, ул. Баумана, д. 15',
    NOW() + INTERVAL '2 days'
),
(
    (SELECT id FROM users WHERE login = 'petrova_anna'),
    (SELECT id FROM users WHERE login = 'kuznetsova_maria'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK003I8J9K0L'),
    'pending',
    'г. Санкт-Петербург, ул. Невский пр., д. 10',
    'г. Новосибирск, ул. Красный пр., д. 20',
    NOW() + INTERVAL '7 days'
),
(
    (SELECT id FROM users WHERE login = 'sidorov_alex'),
    (SELECT id FROM users WHERE login = 'popov_dmitry'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK004M1N2O3P'),
    'in_transit',
    'г. Казань, ул. Баумана, д. 15',
    'г. Екатеринбург, ул. Малышева, д. 5',
    NOW() + INTERVAL '3 days'
),
(
    (SELECT id FROM users WHERE login = 'kuznetsova_maria'),
    (SELECT id FROM users WHERE login = 'volkova_elena'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK005Q4R5S6T'),
    'pending',
    'г. Новосибирск, ул. Красный пр., д. 20',
    'г. Самара, ул. Ленинградская, д. 8',
    NOW() + INTERVAL '5 days'
),
(
    (SELECT id FROM users WHERE login = 'popov_dmitry'),
    (SELECT id FROM users WHERE login = 'novikov_sergey'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK006U7V8W9X'),
    'delivered',
    'г. Екатеринбург, ул. Малышева, д. 5',
    'г. Нижний Новгород, ул. Большая Покровская, д. 12',
    NOW() - INTERVAL '3 days'
),
(
    (SELECT id FROM users WHERE login = 'volkova_elena'),
    (SELECT id FROM users WHERE login = 'morozova_olga'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK007Y0Z1A2B'),
    'in_transit',
    'г. Самара, ул. Ленинградская, д. 8',
    'г. Ростов-на-Дону, ул. Большая Садовая, д. 25',
    NOW() + INTERVAL '4 days'
),
(
    (SELECT id FROM users WHERE login = 'novikov_sergey'),
    (SELECT id FROM users WHERE login = 'lebedev_andrey'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK008C3D4E5F'),
    'pending',
    'г. Нижний Новгород, ул. Большая Покровская, д. 12',
    'г. Уфа, ул. Ленина, д. 30',
    NOW() + INTERVAL '6 days'
),
(
    (SELECT id FROM users WHERE login = 'morozova_olga'),
    (SELECT id FROM users WHERE login = 'kozlova_natalia'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK009G6H7I8J'),
    'cancelled',
    'г. Ростов-на-Дону, ул. Большая Садовая, д. 25',
    'г. Омск, ул. Ленина, д. 18',
    NULL
),
(
    (SELECT id FROM users WHERE login = 'lebedev_andrey'),
    (SELECT id FROM users WHERE login = 'smirnov_pavel'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK010K9L0M1N'),
    'delivered',
    'г. Уфа, ул. Ленина, д. 30',
    'г. Челябинск, ул. Кирова, д. 22',
    NOW() - INTERVAL '1 day'
),
(
    (SELECT id FROM users WHERE login = 'kozlova_natalia'),
    (SELECT id FROM users WHERE login = 'vasileva_irina'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK011O2P3Q4R'),
    'pending',
    'г. Омск, ул. Ленина, д. 18',
    'г. Воронеж, ул. Кольцовская, д. 7',
    NOW() + INTERVAL '8 days'
),
(
    (SELECT id FROM users WHERE login = 'smirnov_pavel'),
    (SELECT id FROM users WHERE login = 'ivanov_ivan'),
    (SELECT id FROM parcels WHERE tracking_number = 'TRK012S5T6U7V'),
    'in_transit',
    'г. Челябинск, ул. Кирова, д. 22',
    'г. Москва, ул. Ленина, д. 1',
    NOW() + INTERVAL '1 day'
);
