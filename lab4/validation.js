
#!/usr/bin/env mongosh
// MongoDB Schema Validation Script для MeowMeowExpress

use delivery;

print("=== Schema Validation Test ===\n");

// ============================================
// Валидация для коллекции users
// ============================================
print("Создание валидации для коллекции users...");

db.createCollection("users", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["login", "first_name", "last_name", "email", "password_hash", "created_at"],
      properties: {
        login: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100,
          pattern: "^[a-zA-Z0-9_]+$",
          description: "Логин пользователя, 1-100 символов, только латиница, цифры и подчёркивание"
        },
        first_name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100,
          description: "Имя пользователя, обязательное поле"
        },
        last_name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100,
          description: "Фамилия пользователя, обязательное поле"
        },
        email: {
          bsonType: "string",
          pattern: "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$",
          description: "Email пользователя в формате user@example.com"
        },
        password_hash: {
          bsonType: "string",
          minLength: 10,
          description: "Хеш пароля, обязательное поле"
        },
        created_at: {
          bsonType: "date",
          description: "Дата создания пользователя"
        },
        updated_at: {
          bsonType: "date",
          description: "Дата последнего обновления"
        }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});

print("✓ Валидация для users создана\n");

// ============================================
// Валидация для коллекции parcels
// ============================================
print("Создание валидации для коллекции parcels...");

db.createCollection("parcels", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["owner_id", "tracking_number", "description", "weight_kg", "dimensions", "created_at"],
      properties: {
        owner_id: {
          bsonType: "objectId",
          description: "Ссылка на пользователя, обязательное поле"
        },
        tracking_number: {
          bsonType: "string",
          minLength: 1,
          maxLength: 50,
          description: "Трек-номер посылки"
        },
        description: {
          bsonType: "string",
          maxLength: 500,
          description: "Описание посылки, максимум 500 символов"
        },
        weight_kg: {
          bsonType: "number",
          minimum: 0,
          maximum: 10000,
          description: "Вес в кг, от 0 до 10000"
        },
        dimensions: {
          bsonType: "string",
          maxLength: 50,
          pattern: "^\\d+x\\d+x\\d+\\s*см$",
          description: "Габариты в формате '10x20x30 см'"
        },
        created_at: {
          bsonType: "date",
          description: "Дата создания посылки"
        },
        updated_at: {
          bsonType: "date",
          description: "Дата последнего обновления"
        }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});

print("✓ Валидация для parcels создана\n");

// ============================================
// Валидация для коллекции deliveries
// ============================================
print("Создание валидации для коллекции deliveries...");

db.createCollection("deliveries", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["sender_id", "recipient_id", "parcel_id", "status", "sender_address", "recipient_address", "created_at"],
      properties: {
        sender_id: {
          bsonType: "objectId",
          description: "Ссылка на отправителя, обязательное поле"
        },
        recipient_id: {
          bsonType: "objectId",
          description: "Ссылка на получателя, обязательное поле"
        },
        parcel_id: {
          bsonType: "objectId",
          description: "Ссылка на посылку, обязательное поле"
        },
        status: {
          bsonType: "string",
          enum: ["pending", "in_transit", "delivered", "cancelled"],
          description: "Статус доставки: pending, in_transit, delivered, cancelled"
        },
        sender_address: {
          bsonType: "string",
          minLength: 1,
          maxLength: 500,
          description: "Адрес отправителя, обязательное поле"
        },
        recipient_address: {
          bsonType: "string",
          minLength: 1,
          maxLength: 500,
          description: "Адрес получателя, обязательное поле"
        },
        estimated_delivery_date: {
          bsonType: "date",
          description: "Планируемая дата доставки"
        },
        actual_delivery_date: {
          bsonType: "date",
          description: "Фактическая дата доставки"
        },
        created_at: {
          bsonType: "date",
          description: "Дата создания доставки"
        },
        updated_at: {
          bsonType: "date",
          description: "Дата последнего обновления"
        }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});

print("✓ Валидация для deliveries создана\n");

// ============================================
// Тестирование валидации
// ============================================
print("\n=== Тестирование валидации ===\n");

// Тест 1: Вставка валидного пользователя (должна пройти)
print("Тест 1: Вставка валидного пользователя...");
try {
  db.users.insertOne({
    login: "test_user",
    first_name: "Тест",
    last_name: "Пользователь",
    email: "test@example.com",
    password_hash: "$2b$12$hashed_password_hash",
    created_at: new Date(),
    updated_at: new Date()
  });
  print("✓ Пользователь успешно вставлен\n");
} catch (e) {
  print("✗ Ошибка: " + e.message + "\n");
}

// Тест 2: Вставка пользователя без login (должна провалиться)
print("Тест 2: Вставка пользователя без login...");
try {
  db.users.insertOne({
    first_name: "Тест",
    last_name: "Пользователь",
    email: "test2@example.com",
    password_hash: "$2b$12$hashed_password_hash",
    created_at: new Date(),
    updated_at: new Date()
  });
  print("✗ Должно было провалиться!\n");
} catch (e) {
  print("✓ Ошибка как ожидалось: " + e.message.split("\n")[0] + "\n");
}

// Тест 3: Вставка пользователя с невалидным email (должна провалиться)
print("Тест 3: Вставка пользователя с невалидным email...");
try {
  db.users.insertOne({
    login: "test_user3",
    first_name: "Тест",
    last_name: "Пользователь",
    email: "invalid-email",
    password_hash: "$2b$12$hashed_password_hash",
    created_at: new Date(),
    updated_at: new Date()
  });
  print("✗ Должно было провалиться!\n");
} catch (e) {
  print("✓ Ошибка как ожидалось: " + e.message.split("\n")[0] + "\n");
}

// Тест 4: Вставка посылки с отрицательным весом (должна провалиться)
print("Тест 4: Вставка посылки с отрицательным весом...");
try {
  db.parcels.insertOne({
    owner_id: ObjectId("507f1f77bcf86cd799439011"),
    tracking_number: "TRK999999",
    description: "Тестовая посылка",
    weight_kg: -1.0,
    dimensions: "10x10x10 см",
    created_at: new Date(),
    updated_at: new Date()
  });
  print("✗ Должно было провалиться!\n");
} catch (e) {
  print("✓ Ошибка как ожидалось: " + e.message.split("\n")[0] + "\n");
}

// Тест 5: Вставка посылки с неверным форматом dimensions (должна провалиться)
print("Тест 5: Вставка посылки с неверным форматом dimensions...");
try {
  db.parcels.insertOne({
    owner_id: ObjectId("507f1f77bcf86cd799439011"),
    tracking_number: "TRK999998",
    description: "Тестовая посылка",
    weight_kg: 1.0,
    dimensions: "Неверный формат",
    created_at: new Date(),
    updated_at: new Date()
  });
  print("✗ Должно было провалиться!\n");
} catch (e) {
  print("✓ Ошибка как ожидалось: " + e.message.split("\n")[0] + "\n");
}

// Тест 6: Вставка доставки с неверным статусом (должна провалиться)
print("Тест 6: Вставка доставки с неверным статусом...");
try {
  db.deliveries.insertOne({
    sender_id: ObjectId("507f1f77bcf86cd799439011"),
    recipient_id: ObjectId("507f1f77bcf86cd799439012"),
    parcel_id: ObjectId("507f1f77bcf86cd799439013"),
    status: "invalid_status",
    sender_address: "Адрес отправителя",
    recipient_address: "Адрес получателя",
    created_at: new Date(),
    updated_at: new Date()
  });
  print("✗ Должно было провалиться!\n");
} catch (e) {
  print("✓ Ошибка как ожидалось: " + e.message.split("\n")[0] + "\n");
}

// Тест 7: Вставка доставки с null sender_address (должна провалиться)
print("Тест 7: Вставка доставки с null sender_address...");
try {
  db.deliveries.insertOne({
    sender_id: ObjectId("507f1f77bcf86cd799439011"),
    recipient_id: ObjectId("507f1f77bcf86cd799439012"),
    parcel_id: ObjectId("507f1f77bcf86cd799439013"),
    status: "pending",
    recipient_address: "Адрес получателя",
    created_at: new Date(),
    updated_at: new Date()
  });
  print("✗ Должно было провалиться!\n");
} catch (e) {
  print("✓ Ошибка как ожидалось: " + e.message.split("\n")[0] + "\n");
}

// Тест 8: Вставка валидной доставки (должна пройти)
print("Тест 8: Вставка валидной доставки...");
try {
  db.deliveries.insertOne({
    sender_id: ObjectId("507f1f77bcf86cd799439011"),
    recipient_id: ObjectId("507f1f77bcf86cd799439012"),
    parcel_id: ObjectId("507f1f77bcf86cd799439013"),
    status: "pending",
    sender_address: "г. Москва, ул. Ленина, д. 1",
    recipient_address: "г. Санкт-Петербург, ул. Невский пр., д. 10",
    estimated_delivery_date: new Date("2026-01-20"),
    created_at: new Date(),
    updated_at: new Date()
  });
  print("✓ Доставка успешно вставлена\n");
} catch (e) {
  print("✗ Ошибка: " + e.message + "\n");
}

// ============================================
// Проверка индексов
// ============================================
print("\n=== Проверка индексов ===\n");

print("Индексы для users:");
db.users.getIndexes().forEach(idx => print("  - " + JSON.stringify(idx.key)));

print("\nИндексы для parcels:");
db.parcels.getIndexes().forEach(idx => print("  - " + JSON.stringify(idx.key)));

print("\nИндексы для deliveries:");
db.deliveries.getIndexes().forEach(idx => print("  - " + JSON.stringify(idx.key)));

// ============================================
// Удаление валидации (опционально)
// ============================================
// print("\nУдаление валидации (для сброса)...");
// db.setCollectionValidation("users", { validator: {} });
// db.setCollectionValidation("parcels", { validator: {} });
// db.setCollectionValidation("deliveries", { validator: {} });
// print("✓ Валидация удалена\n");

print("\n=== Тестирование завершено ===");
