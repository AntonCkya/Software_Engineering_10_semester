(async () => {
  try {
    db = db.getSiblingDB('delivery');

    // === Вспомогательная функция: генерация UUIDv4 как строка ===
    function generateUUIDv4() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.floor(Math.random() * 16);
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    }

    // === Генерация UUID4 для пользователей ===
    const ivanovId = generateUUIDv4();
    const petrovaId = generateUUIDv4();
    const sidorovId = generateUUIDv4();
    const kuznetsovaId = generateUUIDv4();
    const popovId = generateUUIDv4();
    const volkovaId = generateUUIDv4();
    const novikovId = generateUUIDv4();
    const morozovaId = generateUUIDv4();
    const lebedevId = generateUUIDv4();
    const kozlovaId = generateUUIDv4();
    const smirnovId = generateUUIDv4();
    const vasilevaId = generateUUIDv4();

    await db.users.insertMany([
      {
        _id: ivanovId,
        login: "ivanov_ivan",
        first_name: "Иван",
        last_name: "Иванов",
        email: "ivanov@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-01T10:00:00Z"),
        updated_at: ISODate("2026-01-01T10:00:00Z")
      },
      {
        _id: petrovaId,
        login: "petrova_anna",
        first_name: "Анна",
        last_name: "Петрова",
        email: "petrova@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-02T11:30:00Z"),
        updated_at: ISODate("2026-01-02T11:30:00Z")
      },
      {
        _id: sidorovId,
        login: "sidorov_alex",
        first_name: "Александр",
        last_name: "Сидоров",
        email: "sidorov@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-03T09:15:00Z"),
        updated_at: ISODate("2026-01-03T09:15:00Z")
      },
      {
        _id: kuznetsovaId,
        login: "kuznetsova_maria",
        first_name: "Мария",
        last_name: "Кузнецова",
        email: "kuznetsova@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-04T14:20:00Z"),
        updated_at: ISODate("2026-01-04T14:20:00Z")
      },
      {
        _id: popovId,
        login: "popov_dmitry",
        first_name: "Дмитрий",
        last_name: "Попов",
        email: "popov@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-05T08:45:00Z"),
        updated_at: ISODate("2026-01-05T08:45:00Z")
      },
      {
        _id: volkovaId,
        login: "volkova_elena",
        first_name: "Елена",
        last_name: "Волкова",
        email: "volkova@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-06T16:00:00Z"),
        updated_at: ISODate("2026-01-06T16:00:00Z")
      },
      {
        _id: novikovId,
        login: "novikov_sergey",
        first_name: "Сергей",
        last_name: "Новиков",
        email: "novikov@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-07T12:30:00Z"),
        updated_at: ISODate("2026-01-07T12:30:00Z")
      },
      {
        _id: morozovaId,
        login: "morozova_olga",
        first_name: "Ольга",
        last_name: "Морозова",
        email: "morozova@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-08T10:15:00Z"),
        updated_at: ISODate("2026-01-08T10:15:00Z")
      },
      {
        _id: lebedevId,
        login: "lebedev_andrey",
        first_name: "Андрей",
        last_name: "Лебедев",
        email: "lebedev@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-09T15:45:00Z"),
        updated_at: ISODate("2026-01-09T15:45:00Z")
      },
      {
        _id: kozlovaId,
        login: "kozlova_natalia",
        first_name: "Наталья",
        last_name: "Козлова",
        email: "kozlova@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-10T09:00:00Z"),
        updated_at: ISODate("2026-01-10T09:00:00Z")
      },
      {
        _id: smirnovId,
        login: "smirnov_pavel",
        first_name: "Павел",
        last_name: "Смирнов",
        email: "smirnov@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-11T11:20:00Z"),
        updated_at: ISODate("2026-01-11T11:20:00Z")
      },
      {
        _id: vasilevaId,
        login: "vasileva_irina",
        first_name: "Ирина",
        last_name: "Васильева",
        email: "vasileva@example.com",
        password_hash: "$2b$12$LJ3m4ys3Lk0T0RZ8oXaEYuYkZ9qJ5z3xKqV7wH0fG2cD4eF6gH8iJ",
        created_at: ISODate("2026-01-12T14:10:00Z"),
        updated_at: ISODate("2026-01-12T14:10:00Z")
      }
    ]);

    // === Генерация UUID4 для посылок ===
    const parcel1Id = generateUUIDv4();
    const parcel2Id = generateUUIDv4();
    const parcel3Id = generateUUIDv4();
    const parcel4Id = generateUUIDv4();
    const parcel5Id = generateUUIDv4();
    const parcel6Id = generateUUIDv4();
    const parcel7Id = generateUUIDv4();
    const parcel8Id = generateUUIDv4();
    const parcel9Id = generateUUIDv4();
    const parcel10Id = generateUUIDv4();
    const parcel11Id = generateUUIDv4();
    const parcel12Id = generateUUIDv4();

    await db.parcels.insertMany([
      {
        _id: parcel1Id,
        owner_id: ivanovId,
        tracking_number: "TRK001A2B3C4D",
        description: "Документы",
        weight_kg: 0.5,
        dimensions: "30x20x5 см",
        created_at: ISODate("2026-01-15T10:00:00Z"),
        updated_at: ISODate("2026-01-15T10:00:00Z")
      },
      {
        _id: parcel2Id,
        owner_id: ivanovId,
        tracking_number: "TRK002E5F6G7H",
        description: "Книги",
        weight_kg: 3.2,
        dimensions: "40x30x15 см",
        created_at: ISODate("2026-01-16T11:30:00Z"),
        updated_at: ISODate("2026-01-16T11:30:00Z")
      },
      {
        _id: parcel3Id,
        owner_id: petrovaId,
        tracking_number: "TRK003I8J9K0L",
        description: "Одежда",
        weight_kg: 1.5,
        dimensions: "50x40x10 см",
        created_at: ISODate("2026-01-17T09:15:00Z"),
        updated_at: ISODate("2026-01-17T09:15:00Z")
      },
      {
        _id: parcel4Id,
        owner_id: sidorovId,
        tracking_number: "TRK004M1N2O3P",
        description: "Электроника",
        weight_kg: 2.0,
        dimensions: "35x25x10 см",
        created_at: ISODate("2026-01-18T14:20:00Z"),
        updated_at: ISODate("2026-01-18T14:20:00Z")
      },
      {
        _id: parcel5Id,
        owner_id: kuznetsovaId,
        tracking_number: "TRK005Q4R5S6T",
        description: "Косметика",
        weight_kg: 0.8,
        dimensions: "25x20x8 см",
        created_at: ISODate("2026-01-19T08:45:00Z"),
        updated_at: ISODate("2026-01-19T08:45:00Z")
      },
      {
        _id: parcel6Id,
        owner_id: popovId,
        tracking_number: "TRK006U7V8W9X",
        description: "Игрушки",
        weight_kg: 1.2,
        dimensions: "45x35x20 см",
        created_at: ISODate("2026-01-20T16:00:00Z"),
        updated_at: ISODate("2026-01-20T16:00:00Z")
      },
      {
        _id: parcel7Id,
        owner_id: volkovaId,
        tracking_number: "TRK007Y0Z1A2B",
        description: "Обувь",
        weight_kg: 1.0,
        dimensions: "35x25x12 см",
        created_at: ISODate("2026-01-21T12:30:00Z"),
        updated_at: ISODate("2026-01-21T12:30:00Z")
      },
      {
        _id: parcel8Id,
        owner_id: novikovId,
        tracking_number: "TRK008C3D4E5F",
        description: "Спорттовары",
        weight_kg: 5.0,
        dimensions: "60x40x30 см",
        created_at: ISODate("2026-01-22T10:15:00Z"),
        updated_at: ISODate("2026-01-22T10:15:00Z")
      },
      {
        _id: parcel9Id,
        owner_id: morozovaId,
        tracking_number: "TRK009G6H7I8J",
        description: "Посуда",
        weight_kg: 2.5,
        dimensions: "40x30x25 см",
        created_at: ISODate("2026-01-23T15:45:00Z"),
        updated_at: ISODate("2026-01-23T15:45:00Z")
      },
      {
        _id: parcel10Id,
        owner_id: lebedevId,
        tracking_number: "TRK010K9L0M1N",
        description: "Аксессуары",
        weight_kg: 0.3,
        dimensions: "20x15x5 см",
        created_at: ISODate("2026-01-24T09:00:00Z"),
        updated_at: ISODate("2026-01-24T09:00:00Z")
      },
      {
        _id: parcel11Id,
        owner_id: kozlovaId,
        tracking_number: "TRK011O2P3Q4R",
        description: "Подарки",
        weight_kg: 1.8,
        dimensions: "35x25x15 см",
        created_at: ISODate("2026-01-25T11:20:00Z"),
        updated_at: ISODate("2026-01-25T11:20:00Z")
      },
      {
        _id: parcel12Id,
        owner_id: smirnovId,
        tracking_number: "TRK012S5T6U7V",
        description: "Канцтовары",
        weight_kg: 0.7,
        dimensions: "30x20x10 см",
        created_at: ISODate("2026-01-26T14:10:00Z"),
        updated_at: ISODate("2026-01-26T14:10:00Z")
      }
    ]);

    // === Создание доставок с UUID4 ===
    await db.deliveries.insertMany([
      {
        _id: generateUUIDv4(),
        sender_id: ivanovId,
        recipient_id: petrovaId,
        parcel_id: parcel1Id,
        status: "delivered",
        sender_address: "г. Москва, ул. Ленина, д. 1",
        recipient_address: "г. Санкт-Петербург, ул. Невский пр., д. 10",
        estimated_delivery_date: ISODate("2026-01-20T10:00:00Z"),
        actual_delivery_date: ISODate("2026-01-20T14:00:00Z"),
        created_at: ISODate("2026-01-15T10:00:00Z"),
        updated_at: ISODate("2026-01-20T14:00:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: ivanovId,
        recipient_id: sidorovId,
        parcel_id: parcel2Id,
        status: "in_transit",
        sender_address: "г. Москва, ул. Ленина, д. 1",
        recipient_address: "г. Казань, ул. Баумана, д. 15",
        estimated_delivery_date: ISODate("2026-01-20T10:00:00Z"),
        created_at: ISODate("2026-01-16T11:30:00Z"),
        updated_at: ISODate("2026-01-16T11:30:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: petrovaId,
        recipient_id: kuznetsovaId,
        parcel_id: parcel3Id,
        status: "pending",
        sender_address: "г. Санкт-Петербург, ул. Невский пр., д. 10",
        recipient_address: "г. Новосибирск, ул. Красный пр., д. 20",
        estimated_delivery_date: ISODate("2026-01-26T10:00:00Z"),
        created_at: ISODate("2026-01-17T09:15:00Z"),
        updated_at: ISODate("2026-01-17T09:15:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: sidorovId,
        recipient_id: popovId,
        parcel_id: parcel4Id,
        status: "in_transit",
        sender_address: "г. Казань, ул. Баумана, д. 15",
        recipient_address: "г. Екатеринбург, ул. Малышева, д. 5",
        estimated_delivery_date: ISODate("2026-01-23T10:00:00Z"),
        created_at: ISODate("2026-01-18T14:20:00Z"),
        updated_at: ISODate("2026-01-18T14:20:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: kuznetsovaId,
        recipient_id: volkovaId,
        parcel_id: parcel5Id,
        status: "pending",
        sender_address: "г. Новосибирск, ул. Красный пр., д. 20",
        recipient_address: "г. Самара, ул. Ленинградская, д. 8",
        estimated_delivery_date: ISODate("2026-01-26T10:00:00Z"),
        created_at: ISODate("2026-01-19T08:45:00Z"),
        updated_at: ISODate("2026-01-19T08:45:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: popovId,
        recipient_id: novikovId,
        parcel_id: parcel6Id,
        status: "delivered",
        sender_address: "г. Екатеринбург, ул. Малышева, д. 5",
        recipient_address: "г. Нижний Новгород, ул. Большая Покровская, д. 12",
        estimated_delivery_date: ISODate("2026-01-25T10:00:00Z"),
        actual_delivery_date: ISODate("2026-01-24T12:00:00Z"),
        created_at: ISODate("2026-01-20T16:00:00Z"),
        updated_at: ISODate("2026-01-24T12:00:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: volkovaId,
        recipient_id: morozovaId,
        parcel_id: parcel7Id,
        status: "in_transit",
        sender_address: "г. Самара, ул. Ленинградская, д. 8",
        recipient_address: "г. Ростов-на-Дону, ул. Большая Садовая, д. 25",
        estimated_delivery_date: ISODate("2026-01-27T10:00:00Z"),
        created_at: ISODate("2026-01-21T12:30:00Z"),
        updated_at: ISODate("2026-01-21T12:30:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: novikovId,
        recipient_id: lebedevId,
        parcel_id: parcel8Id,
        status: "pending",
        sender_address: "г. Нижний Новгород, ул. Большая Покровская, д. 12",
        recipient_address: "г. Уфа, ул. Ленина, д. 30",
        estimated_delivery_date: ISODate("2026-01-29T10:00:00Z"),
        created_at: ISODate("2026-01-22T10:15:00Z"),
        updated_at: ISODate("2026-01-22T10:15:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: morozovaId,
        recipient_id: kozlovaId,
        parcel_id: parcel9Id,
        status: "cancelled",
        sender_address: "г. Ростов-на-Дону, ул. Большая Садовая, д. 25",
        recipient_address: "г. Омск, ул. Ленина, д. 18",
        estimated_delivery_date: ISODate("2026-01-28T10:00:00Z"),
        created_at: ISODate("2026-01-23T15:45:00Z"),
        updated_at: ISODate("2026-01-25T09:00:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: lebedevId,
        recipient_id: smirnovId,
        parcel_id: parcel10Id,
        status: "delivered",
        sender_address: "г. Уфа, ул. Ленина, д. 30",
        recipient_address: "г. Челябинск, ул. Кирова, д. 22",
        estimated_delivery_date: ISODate("2026-01-27T10:00:00Z"),
        actual_delivery_date: ISODate("2026-01-26T16:00:00Z"),
        created_at: ISODate("2026-01-24T09:00:00Z"),
        updated_at: ISODate("2026-01-26T16:00:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: kozlovaId,
        recipient_id: vasilevaId,
        parcel_id: parcel11Id,
        status: "pending",
        sender_address: "г. Омск, ул. Ленина, д. 18",
        recipient_address: "г. Воронеж, ул. Кольцовская, д. 7",
        estimated_delivery_date: ISODate("2026-01-30T10:00:00Z"),
        created_at: ISODate("2026-01-25T11:20:00Z"),
        updated_at: ISODate("2026-01-25T11:20:00Z")
      },
      {
        _id: generateUUIDv4(),
        sender_id: smirnovId,
        recipient_id: ivanovId,
        parcel_id: parcel12Id,
        status: "in_transit",
        sender_address: "г. Челябинск, ул. Кирова, д. 22",
        recipient_address: "г. Москва, ул. Ленина, д. 1",
        estimated_delivery_date: ISODate("2026-01-28T10:00:00Z"),
        created_at: ISODate("2026-01-26T14:10:00Z"),
        updated_at: ISODate("2026-01-26T14:10:00Z")
      }
    ]);

    // === Создание индексов ===
    await db.users.createIndex({ login: 1 }, { unique: true });
    await db.users.createIndex({ email: 1 }, { unique: true });
    await db.users.createIndex({ first_name: 1 });
    await db.users.createIndex({ last_name: 1 });

    await db.parcels.createIndex({ owner_id: 1 });
    await db.parcels.createIndex({ tracking_number: 1 }, { unique: true });

    await db.deliveries.createIndex({ sender_id: 1 });
    await db.deliveries.createIndex({ recipient_id: 1 });
    await db.deliveries.createIndex({ parcel_id: 1 });
    await db.deliveries.createIndex({ status: 1, created_at: -1 });

    print("✅ Database initialization completed!");
    print("Collections created:");
    print("- users: " + db.users.countDocuments() + " documents");
    print("- parcels: " + db.parcels.countDocuments() + " documents");
    print("- deliveries: " + db.deliveries.countDocuments() + " documents");
    print("\n💡 All documents now use UUID4 as _id field");
  } catch (err) {
    print("❌ Initialization error: " + err.message);
    printjson(err);
    throw err;
  }
})();