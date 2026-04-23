#!/usr/bin/env mongosh
// MongoDB initialization script for MeowMeowExpress

use delivery;

// Создание пользователей
db.users.insertMany([
  {
    login: "ivanov_ivan",
    first_name: "Иван",
    last_name: "Иванов",
    email: "ivanov@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-01T10:00:00Z"),
    updated_at: ISODate("2026-01-01T10:00:00Z")
  },
  {
    login: "petrova_anna",
    first_name: "Анна",
    last_name: "Петрова",
    email: "petrova@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-02T11:30:00Z"),
    updated_at: ISODate("2026-01-02T11:30:00Z")
  },
  {
    login: "sidorov_alex",
    first_name: "Александр",
    last_name: "Сидоров",
    email: "sidorov@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-03T09:15:00Z"),
    updated_at: ISODate("2026-01-03T09:15:00Z")
  },
  {
    login: "kuznetsova_maria",
    first_name: "Мария",
    last_name: "Кузнецова",
    email: "kuznetsova@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-04T14:20:00Z"),
    updated_at: ISODate("2026-01-04T14:20:00Z")
  },
  {
    login: "popov_dmitry",
    first_name: "Дмитрий",
    last_name: "Попов",
    email: "popov@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-05T08:45:00Z"),
    updated_at: ISODate("2026-01-05T08:45:00Z")
  },
  {
    login: "volkova_elena",
    first_name: "Елена",
    last_name: "Волкова",
    email: "volkova@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-06T16:00:00Z"),
    updated_at: ISODate("2026-01-06T16:00:00Z")
  },
  {
    login: "novikov_sergey",
    first_name: "Сергей",
    last_name: "Новиков",
    email: "novikov@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-07T12:30:00Z"),
    updated_at: ISODate("2026-01-07T12:30:00Z")
  },
  {
    login: "morozova_olga",
    first_name: "Ольга",
    last_name: "Морозова",
    email: "morozova@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-08T10:15:00Z"),
    updated_at: ISODate("2026-01-08T10:15:00Z")
  },
  {
    login: "lebedev_andrey",
    first_name: "Андрей",
    last_name: "Лебедев",
    email: "lebedev@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-09T15:45:00Z"),
    updated_at: ISODate("2026-01-09T15:45:00Z")
  },
  {
    login: "kozlova_natalia",
    first_name: "Наталья",
    last_name: "Козлова",
    email: "kozlova@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-10T09:00:00Z"),
    updated_at: ISODate("2026-01-10T09:00:00Z")
  },
  {
    login: "smirnov_pavel",
    first_name: "Павел",
    last_name: "Смирнов",
    email: "smirnov@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-11T11:20:00Z"),
    updated_at: ISODate("2026-01-11T11:20:00Z")
  },
  {
    login: "vasileva_irina",
    first_name: "Ирина",
    last_name: "Васильева",
    email: "vasileva@example.com",
    password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
    created_at: ISODate("2026-01-12T14:10:00Z"),
    updated_at: ISODate("2026-01-12T14:10:00Z")
  }
]);

// Получение ObjectId пользователей для ссылок
const users = db.users.find({}, { _id: 1, login: 1 }).toArray();
const ivanovId = users.find(u => u.login === "ivanov_ivan")._id;
const petrovaId = users.find(u => u.login === "petrova_anna")._id;
const sidorovId = users.find(u => u.login === "sidorov_alex")._id;
const kuznetsovaId = users.find(u => u.login === "kuznetsova_maria")._id;
const popovId = users.find(u => u.login === "popov_dmitry")._id;
const volkovaId = users.find(u => u.login === "volkova_elena")._id;
const novikovId = users.find(u => u.login === "novikov_sergey")._id;
const morozovaId = users.find(u => u.login === "morozova_olga")._id;
const lebedevId = users.find(u => u.login === "lebedev_andrey")._id;
const kozlovaId = users.find(u => u.login === "kozlova_natalia")._id;
const smirnovId = users.find(u => u.login === "smirnov_pavel")._id;
const vasilevaId = users.find(u => u.login === "vasileva_irina")._id;

// Создание посылок
db.parcels.insertMany([
  {
    owner_id: ivanovId,
    tracking_number: "TRK001A2B3C4D",
    description: "Документы",
    weight_kg: 0.5,
    dimensions: "30x20x5 см",
    created_at: ISODate("2026-01-15T10:00:00Z"),
    updated_at: ISODate("2026-01-15T10:00:00Z")
  },
  {
    owner_id: ivanovId,
    tracking_number: "TRK002E5F6G7H",
    description: "Книги",
    weight_kg: 3.2,
    dimensions: "40x30x15 см",
    created_at: ISODate("2026-01-16T11:30:00Z"),
    updated_at: ISODate("2026-01-16T11:30:00Z")
  },
  {
    owner_id: petrovaId,
    tracking_number: "TRK003I8J9K0L",
    description: "Одежда",
    weight_kg: 1.5,
    dimensions: "50x40x10 см",
    created_at: ISODate("2026-01-17T09:15:00Z"),
    updated_at: ISODate("2026-01-17T09:15:00Z")
  },
  {
    owner_id: sidorovId,
    tracking_number: "TRK004M1N2O3P",
    description: "Электроника",
    weight_kg: 2.0,
    dimensions: "35x25x10 см",
    created_at: ISODate("2026-01-18T14:20:00Z"),
    updated_at: ISODate("2026-01-18T14:20:00Z")
  },
  {
    owner_id: kuznetsovaId,
    tracking_number: "TRK005Q4R5S6T",
    description: "Косметика",
    weight_kg: 0.8,
    dimensions: "25x20x8 см",
    created_at: ISODate("2026-01-19T08:45:00Z"),
    updated_at: ISODate("2026-01-19T08:45:00Z")
  },
  {
    owner_id: popovId,
    tracking_number: "TRK006U7V8W9X",
    description: "Игрушки",
    weight_kg: 1.2,
    dimensions: "45x35x20 см",
    created_at: ISODate("2026-01-20T16:00:00Z"),
    updated_at: ISODate("2026-01-20T16:00:00Z")
  },
  {
    owner_id: volkovaId,
    tracking_number: "TRK007Y0Z1A2B",
    description: "Обувь",
    weight_kg: 1.0,
    dimensions: "35x25x12 см",
    created_at: ISODate("2026-01-21T12:30:00Z"),
    updated_at: ISODate("2026-01-21T12:30:00Z")
  },
  {
    owner_id: novikovId,
    tracking_number: "TRK008C3D4E5F",
    description: "Спорттовары",
    weight_kg: 5.0,
    dimensions: "60x40x30 см",
    created_at: ISODate("2026-01-22T10:15:00Z"),
    updated_at: ISODate("2026-01-22T10:15:00Z")
  },
  {
    owner_id: morozovaId,
    tracking_number: "TRK009G6H7I8J",
    description: "Посуда",
    weight_kg: 2.5,
    dimensions: "40x30x25 см",
    created_at: ISODate("2026-01-23T15:45:00Z"),
    updated_at: ISODate("2026-01-23T15:45:00Z")
  },
  {
    owner_id: lebedevId,
    tracking_number: "TRK010K9L0M1N",
    description: "Аксессуары",
    weight_kg: 0.3,
    dimensions: "20x15x5 см",
    created_at: ISODate("2026-01-24T09:00:00Z"),
    updated_at: ISODate("2026-01-24T09:00:00Z")
  },
  {
    owner_id: kozlovaId,
    tracking_number: "TRK011O2P3Q4R",
    description: "Подарки",
    weight_kg: 1.8,
    dimensions: "35x25x15 см",
    created_at: ISODate("2026-01-25T11:20:00Z"),
    updated_at: ISODate("2026-01-25T11:20:00Z")
  },
  {
    owner_id: smirnovId,
    tracking_number: "TRK012S5T6U7V",
    description: "Канцтовары",
    weight_kg: 0.7,
    dimensions: "30x20x10 см",
    created_at: ISODate("2026-01-26T14:10:00Z"),
    updated_at: ISODate("2026-01-26T14:10:00Z")
  }
]);

// Получение ObjectId посылок
const parcels = db.parcels.find({}, { _id: 1, tracking_number: 1 }).toArray();
const parcel1 = parcels.find(p => p.tracking_number === "TRK001A2B3C4D")._id;
const parcel2 = parcels.find(p => p.tracking_number === "TRK002E5F6G7H")._id;
const parcel3 = parcels.find(p => p.tracking_number === "TRK003I8J9K0L")._id;
const parcel4 = parcels.find(p => p.tracking_number === "TRK004M1N2O3P")._id;
const parcel5 = parcels.find(p => p.tracking_number === "TRK005Q4R5S6T")._id;
const parcel6 = parcels.find(p => p.tracking_number === "TRK006U7V8W9X")._id;
const parcel7 = parcels.find(p => p.tracking_number === "TRK007Y0Z1A2B")._id;
const parcel8 = parcels.find(p => p.tracking_number === "TRK008C3D4E5F")._id;
const parcel9 = parcels.find(p => p.tracking_number === "TRK009G6H7I8J")._id;
const parcel10 = parcels.find(p => p.tracking_number === "TRK010K9L0M1N")._id;
const parcel11 = parcels.find(p => p.tracking_number === "TRK011O2P3Q4R")._id;
const parcel12 = parcels.find(p => p.tracking_number === "TRK012S5T6U7V")._id;

// Создание доставок
db.deliveries.insertMany([
  {
    sender_id: ivanovId,
    recipient_id: petrovaId,
    parcel_id: parcel1,
    status: "delivered",
    sender_address: "г. Москва, ул. Ленина, д. 1",
    recipient_address: "г. Санкт-Петербург, ул. Невский пр., д. 10",
    estimated_delivery_date: ISODate("2026-01-20T10:00:00Z"),
    actual_delivery_date: ISODate("2026-01-20T14:00:00Z"),
    created_at: ISODate("2026-01-15T10:00:00Z"),
    updated_at: ISODate("2026-01-20T14:00:00Z")
  },
  {
    sender_id: ivanovId,
    recipient_id: sidorovId,
    parcel_id: parcel2,
    status: "in_transit",
    sender_address: "г. Москва, ул. Ленина, д. 1",
    recipient_address: "г. Казань, ул. Баумана, д. 15",
    estimated_delivery_date: ISODate("2026-01-20T10:00:00Z"),
    created_at: ISODate("2026-01-16T11:30:00Z"),
    updated_at: ISODate("2026-01-16T11:30:00Z")
  },
  {
    sender_id: petrovaId,
    recipient_id: kuznetsovaId,
    parcel_id: parcel3,
    status: "pending",
    sender_address: "г. Санкт-Петербург, ул. Невский пр., д. 10",
    recipient_address: "г. Новосибирск, ул. Красный пр., д. 20",
    estimated_delivery_date: ISODate("2026-01-26T10:00:00Z"),
    created_at: ISODate("2026-01-17T09:15:00Z"),
    updated_at: ISODate("2026-01-17T09:15:00Z")
  },
  {
    sender_id: sidorovId,
    recipient_id: popovId,
    parcel_id: parcel4,
    status: "in_transit",
    sender_address: "г. Казань, ул. Баумана, д. 15",
    recipient_address: "г. Екатеринбург, ул. Малышева, д. 5",
    estimated_delivery_date: ISODate("2026-01-23T10:00:00Z"),
    created_at: ISODate("2026-01-18T14:20:00Z"),
    updated_at: ISODate("2026-01-18T14:20:00Z")
  },
  {
    sender_id: kuznetsovaId,
    recipient_id: volkovaId,
    parcel_id: parcel5,
    status: "pending",
    sender_address: "г. Новосибирск, ул. Красный пр., д. 20",
    recipient_address: "г. Самара, ул. Ленинградская, д. 8",
    estimated_delivery_date: ISODate("2026-01-26T10:00:00Z"),
    created_at: ISODate("2026-01-19T08:45:00Z"),
    updated_at: ISODate("2026-01-19T08:45:00Z")
  },
  {
    sender_id: popovId,
    recipient_id: novikovId,
    parcel_id: parcel6,
    status: "delivered",
    sender_address: "г. Екатеринбург, ул. Малышева, д. 5",
    recipient_address: "г. Нижний Новгород, ул. Большая Покровская, д. 12",
    estimated_delivery_date: ISODate("2026-01-25T10:00:00Z"),
    actual_delivery_date: ISODate("2026-01-24T12:00:00Z"),
    created_at: ISODate("2026-01-20T16:00:00Z"),
    updated_at: ISODate("2026-01-24T12:00:00Z")
  },
  {
    sender_id: volkovaId,
    recipient_id: morozovaId,
    parcel_id: parcel7,
    status: "in_transit",
    sender_address: "г. Самара, ул. Ленинградская, д. 8",
    recipient_address: "г. Ростов-на-Дону, ул. Большая Садовая, д. 25",
    estimated_delivery_date: ISODate("2026-01-27T10:00:00Z"),
    created_at: ISODate("2026-01-21T12:30:00Z"),
    updated_at: ISODate("2026-01-21T12:30:00Z")
  },
  {
    sender_id: novikovId,
    recipient_id: lebedevId,
    parcel_id: parcel8,
    status: "pending",
    sender_address: "г. Нижний Новгород, ул. Большая Покровская, д. 12",
    recipient_address: "г. Уфа, ул. Ленина, д. 30",
    estimated_delivery_date: ISODate("2026-01-29T10:00:00Z"),
    created_at: ISODate("2026-01-22T10:15:00Z"),
    updated_at: ISODate("2026-01-22T10:15:00Z")
  },
  {
    sender_id: morozovaId,
    recipient_id: kozlovaId,
    parcel_id: parcel9,
    status: "cancelled",
    sender_address: "г. Ростов-на-Дону, ул. Большая Садовая, д. 25",
    recipient_address: "г. Омск, ул. Ленина, д. 18",
    estimated_delivery_date: ISODate("2026-01-28T10:00:00Z"),
    created_at: ISODate("2026-01-23T15:45:00Z"),
    updated_at: ISODate("2026-01-25T09:00:00Z")
  },
  {
    sender_id: lebedevId,
    recipient_id: smirnovId,
    parcel_id: parcel10,
    status: "delivered",
    sender_address: "г. Уфа, ул. Ленина, д. 30",
    recipient_address: "г. Челябинск, ул. Кирова, д. 22",
    estimated_delivery_date: ISODate("2026-01-27T10:00:00Z"),
    actual_delivery_date: ISODate("2026-01-26T16:00:00Z"),
    created_at: ISODate("2026-01-24T09:00:00Z"),
    updated_at: ISODate("2026-01-26T16:00:00Z")
  },
  {
    sender_id: kozlovaId,
    recipient_id: vasilevaId,
    parcel_id: parcel11,
    status: "pending",
    sender_address: "г. Омск, ул. Ленина, д. 18",
    recipient_address: "г. Воронеж, ул. Кольцовская, д. 7",
    estimated_delivery_date: ISODate("2026-01-30T10:00:00Z"),
    created_at: ISODate("2026-01-25T11:20:00Z"),
    updated_at: ISODate("2026-01-25T11:20:00Z")
  },
  {
    sender_id: smirnovId,
    recipient_id: ivanovId,
    parcel_id: parcel12,
    status: "in_transit",
    sender_address: "г. Челябинск, ул. Кирова, д. 22",
    recipient_address: "г. Москва, ул. Ленина, д. 1",
    estimated_delivery_date: ISODate("2026-01-28T10:00:00Z"),
    created_at: ISODate("2026-01-26T14:10:00Z"),
    updated_at: ISODate("2026-01-26T14:10:00Z")
  }
]);

// Создание индексов
db.users.createIndex({ login: 1 }, { unique: true });
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ first_name: 1 });
db.users.createIndex({ last_name: 1 });

db.parcels.createIndex({ owner_id: 1 });
db.parcels.createIndex({ tracking_number: 1 }, { unique: true });

db.deliveries.createIndex({ sender_id: 1 });
db.deliveries.createIndex({ recipient_id: 1 });
db.deliveries.createIndex({ parcel_id: 1 });
db.deliveries.createIndex({ status: 1, created_at: -1 });

print("Database initialization completed!");
print("Collections created:");
print("- users: " + db.users.countDocuments() + " documents");
print("- parcels: " + db.parcels.countDocuments() + " documents");
print("- deliveries: " + db.deliveries.countDocuments() + " documents");