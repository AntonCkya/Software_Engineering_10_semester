db = db.getSiblingDB('delivery');

print("=== Schema Validation Test ===\n");

// ============================================
// Валидация для коллекции users
// ============================================
print("Создание валидации для коллекции users...");

const usersValidationResult = db.runCommand({
  collMod: "users",
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
          description: "Логин пользователя"
        },
        first_name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100
        },
        last_name: {
          bsonType: "string",
          minLength: 1,
          maxLength: 100
        },
        email: {
          bsonType: "string",
          pattern: "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
        },
        password_hash: {
          bsonType: "string",
          minLength: 10
        },
        created_at: { bsonType: "date" },
        updated_at: { bsonType: "date" }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
});

if (usersValidationResult.ok === 1) {
  print("✓ Валидация для users применена\n");
} else {
  print("✗ Ошибка применения валидации: " + JSON.stringify(usersValidationResult) + "\n");
}

// ============================================
// Валидация для коллекции parcels
// ============================================
print("Создание валидации для коллекции parcels...");

const parcelsValidationResult = db.runCommand({
  collMod: "parcels",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["owner_id", "tracking_number", "description", "weight_kg", "dimensions", "created_at"],
      properties: {
        owner_id: {
          bsonType: "string",
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
print(parcelsValidationResult.ok === 1 ? "✓ parcels\n" : "✗ parcels: " + JSON.stringify(parcelsValidationResult) + "\n");

// ============================================
// Валидация для коллекции deliveries
// ============================================
print("Создание валидации для коллекции deliveries...");

const deliveriesValidationResult = db.runCommand({
  collMod: "deliveries",
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["sender_id", "recipient_id", "parcel_id", "status", "sender_address", "recipient_address", "created_at"],
      properties: {
        sender_id: {
          bsonType: "string",
          description: "Ссылка на отправителя, обязательное поле"
        },
        recipient_id: {
          bsonType: "string",
          description: "Ссылка на получателя, обязательное поле"
        },
        parcel_id: {
          bsonType: "string",
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

print(deliveriesValidationResult.ok === 1 ? "✓ deliveries\n" : "✗ deliveries: " + JSON.stringify(deliveriesValidationResult) + "\n");

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
    owner_id: "90f7441c-8215-43b4-8533-277460573af6",
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
    owner_id: "90f7441c-8215-43b4-8533-277460573af6",
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
    sender_id: "90f7441c-8215-43b4-8533-277460573af6",
    recipient_id: "90f7441c-8215-43b4-8533-277460573af6",
    parcel_id: "90f7441c-8215-43b4-8533-277460573af6",
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
    sender_id: "90f7441c-8215-43b4-8533-277460573af6",
    recipient_id: "90f7441c-8215-43b4-8533-277460573af6",
    parcel_id: "90f7441c-8215-43b4-8533-277460573af6",
    status: "pending",
    recipient_address: "Адрес получателя",
    created_at: new Date(),
    updated_at: new Date()
  });
  print("✗ Должно было провалиться!\n");
} catch (e) {
  print("✓ Ошибка как ожидалось: " + e.message.split("\n")[0] + "\n");
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
