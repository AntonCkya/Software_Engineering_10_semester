db = db.getSiblingDB('delivery');

print("\n🚀 Запуск скрипта MeowMeowExpress...\n");

// ----------------------------------------------------------------------------
// 1. СОЗДАНИЕ ИНДЕКСОВ
// ----------------------------------------------------------------------------
print("📌 Создание индексов для коллекции users...");
try {
  db.users.createIndex({ login: 1 }, { unique: true });
  db.users.createIndex({ email: 1 }, { unique: true });
  db.users.createIndex({ first_name: 1 });
  db.users.createIndex({ last_name: 1 });
  db.users.createIndex({ created_at: -1 });
  print("✅ Индексы для users созданы успешно");
} catch (e) {
  print("❌ Ошибка при создании индексов users: " + e.message);
}

print("\n📌 Создание индексов для коллекции parcels...");
try {
  db.parcels.createIndex({ owner_id: 1 });
  db.parcels.createIndex({ tracking_number: 1 }, { unique: true });
  db.parcels.createIndex({ created_at: -1 });
  print("✅ Индексы для parcels созданы успешно");
} catch (e) {
  print("❌ Ошибка при создании индексов parcels: " + e.message);
}

print("\n📌 Создание индексов для коллекции deliveries...");
try {
  db.deliveries.createIndex({ sender_id: 1 });
  db.deliveries.createIndex({ recipient_id: 1 });
  db.deliveries.createIndex({ parcel_id: 1 });
  db.deliveries.createIndex({ status: 1, created_at: -1 });
  print("✅ Индексы для deliveries созданы успешно");
} catch (e) {
  print("❌ Ошибка при создании индексов deliveries: " + e.message);
}

// ----------------------------------------------------------------------------
// 2. CREATE — Вставка документов
// ----------------------------------------------------------------------------
print("\n📦 Вставка тестового пользователя...");
const testUser = db.users.insertOne({
  _id: "550e8400-e29b-41d4-a716-446655440000",
  login: "new_user",
  first_name: "Новый",
  last_name: "Пользователь",
  email: "newuser@example.com",
  password_hash: "$2b$12$hashed_password",
  created_at: new Date(),
  updated_at: new Date()
});
print(testUser.acknowledged && testUser.insertedId 
  ? "✅ Пользователь вставлен: " + testUser.insertedId 
  : "❌ Не удалось вставить пользователя");

print("\n📦 Вставка нескольких пользователей...");
const bulkUsers = db.users.insertMany([
  {
    _id: "550e8400-e29b-41d4-a716-446655440001",
    login: "user1",
    first_name: "Иван",
    last_name: "Иванов",
    email: "user1@example.com",
    password_hash: "$2b$12$hash1",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    _id: "550e8400-e29b-41d4-a716-446655440002",
    login: "user2",
    first_name: "Петр",
    last_name: "Петров",
    email: "user2@example.com",
    password_hash: "$2b$12$hash2",
    created_at: new Date(),
    updated_at: new Date()
  }
]);
print(bulkUsers.acknowledged && bulkUsers.insertedIds 
  ? "✅ Вставлено пользователей: " + Object.keys(bulkUsers.insertedIds).length 
  : "❌ Не удалось вставить пользователей");

print("\n📦 Вставка посылки...");
const parcel = db.parcels.insertOne({
  _id: "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  owner_id: "550e8400-e29b-41d4-a716-446655440000",
  tracking_number: "TRK123456789",
  description: "Новая посылка",
  weight_kg: 2.5,
  dimensions: "30x20x15 см",
  created_at: new Date(),
  updated_at: new Date()
});
print(parcel.acknowledged && parcel.insertedId 
  ? "✅ Посылка вставлена: " + parcel.insertedId 
  : "❌ Не удалось вставить посылку");

print("\n📦 Вставка доставки...");
const delivery = db.deliveries.insertOne({
  _id: "7c9e6679-7425-40de-944b-e07fc1f90ae7",
  sender_id: "550e8400-e29b-41d4-a716-446655440000",
  recipient_id: "550e8400-e29b-41d4-a716-446655440001",
  parcel_id: "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  status: "pending",
  sender_address: "г. Москва, ул. Ленина, д. 1",
  recipient_address: "г. Санкт-Петербург, ул. Невский пр., д. 10",
  estimated_delivery_date: new Date("2026-01-20"),
  created_at: new Date(),
  updated_at: new Date()
});
print(delivery.acknowledged && delivery.insertedId 
  ? "✅ Доставка вставлена: " + delivery.insertedId 
  : "❌ Не удалось вставить доставку");

// ----------------------------------------------------------------------------
// 3. READ — Поиск документов
// ----------------------------------------------------------------------------
print("\n🔍 Поиск пользователя по login...");
const userByLogin = db.users.findOne({ login: "new_user" });
print(userByLogin 
  ? "✅ Найдено: " + JSON.stringify({ login: userByLogin.login, name: userByLogin.first_name }) 
  : "❌ Пользователь не найден");

print("\n🔍 Поиск посылок пользователя по owner_id...");
const userParcels = db.parcels.find({ owner_id: "550e8400-e29b-41d4-a716-446655440000" }).toArray();
print("✅ Найдено посылок: " + userParcels.length);

print("\n🔍 Поиск доставок по статусу с сортировкой...");
const pendingDeliveries = db.deliveries.find({ status: "pending" })
  .sort({ created_at: -1 }).toArray();
print("✅ Найдено доставок в статусе 'pending': " + pendingDeliveries.length);

print("\n🔍 Поиск пользователей по маске имени (регулярное выражение)...");
const usersByPattern = db.users.find({ 
  first_name: { $regex: ".*ан.*", $options: "i" }
}).toArray();
print("✅ Найдено пользователей по маске: " + usersByPattern.length);

print("\n🔍 Поиск доставок с весом посылки > 2.0 кг ($lookup)...");
const heavyDeliveries = db.deliveries.aggregate([
  {
    $lookup: {
      from: "parcels",
      localField: "parcel_id",
      foreignField: "_id",
      as: "parcel"
    }
  },
  { $unwind: "$parcel" },
  { $match: { "parcel.weight_kg": { $gt: 2.0 } } }
]).toArray();
print("✅ Найдено доставок с тяжёлыми посылками: " + heavyDeliveries.length);

// ----------------------------------------------------------------------------
// 4. UPDATE — Обновление документов
// ----------------------------------------------------------------------------
print("\n✏️ Обновление пользователя по _id...");
const updateUser = db.users.updateOne(
  { _id: "550e8400-e29b-41d4-a716-446655440000" },
  {
    $set: {
      first_name: "Иван",
      last_name: "Иванов",
      updated_at: new Date()
    }
  }
);
print(updateUser.modifiedCount > 0 
  ? "✅ Обновлено документов: " + updateUser.modifiedCount 
  : "⚠️ Документ не изменён или не найден");

print("\n✏️ Обновление статуса доставки...");
const updateDelivery = db.deliveries.updateOne(
  { _id: "7c9e6679-7425-40de-944b-e07fc1f90ae7" },
  {
    $set: {
      status: "in_transit",
      updated_at: new Date()
    }
  }
);
print(updateDelivery.modifiedCount > 0 
  ? "✅ Статус доставки обновлён" 
  : "⚠️ Доставка не найдена или не изменена");

print("\n✏️ Увеличение веса посылки ($inc)...");
const incWeight = db.parcels.updateOne(
  { _id: "6ba7b810-9dad-11d1-80b4-00c04fd430c8" },
  { $inc: { weight_kg: 0.5 } }
);
print(incWeight.modifiedCount > 0 
  ? "✅ Вес посылки увеличен" 
  : "⚠️ Посылка не найдена");

print("\n✏️ Добавление тега в массив ($addToSet)...");
const addTag = db.users.updateOne(
  { _id: "550e8400-e29b-41d4-a716-446655440000" },
  { $addToSet: { tags: "vip" } }
);
print(addTag.modifiedCount >= 0 
  ? "✅ Операция с массивом выполнена" 
  : "❌ Ошибка при обновлении массива");

print("\n✏️ Массовое обновление доставок ($updateMany)...");
const bulkUpdate = db.deliveries.updateMany(
  { status: "pending" },
  { $set: { status: "in_transit", updated_at: new Date() } }
);
print("✅ Обновлено доставок: " + bulkUpdate.modifiedCount);

// ----------------------------------------------------------------------------
// 5. DELETE — Удаление документов
// ----------------------------------------------------------------------------
print("\n🗑️ Удаление пользователя по _id...");
// Сначала удалим зависимые записи
db.deliveries.deleteMany({ 
  $or: [
    { sender_id: "550e8400-e29b-41d4-a716-446655440002" },
    { recipient_id: "550e8400-e29b-41d4-a716-446655440002" }
  ]
});
db.parcels.deleteMany({ owner_id: "550e8400-e29b-41d4-a716-446655440002" });

const deleteUser = db.users.deleteOne({ _id: "550e8400-e29b-41d4-a716-446655440002" });
print(deleteUser.deletedCount > 0 
  ? "✅ Пользователь удалён" 
  : "⚠️ Пользователь не найден");

print("\n🗑️ Удаление доставок со статусом 'cancelled'...");
const deleteCancelled = db.deliveries.deleteMany({ status: "cancelled" });
print("✅ Удалено отменённых доставок: " + deleteCancelled.deletedCount);

// ----------------------------------------------------------------------------
// 6. АГРЕГАЦИЯ
// ----------------------------------------------------------------------------
print("\n📊 Подсчёт количества посылок у каждого пользователя...");
const parcelsPerUser = db.parcels.aggregate([
  { $group: { _id: "$owner_id", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
]).toArray();
print("✅ Пользователей с посылками: " + parcelsPerUser.length);
parcelsPerUser.forEach(u => print("   • " + u._id + ": " + u.count + " посылок"));

print("\n📊 Статистика доставок по статусу...");
const statusStats = db.deliveries.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
]).toArray();
print("✅ Статусов найдено: " + statusStats.length);
statusStats.forEach(s => print("   • " + s._id + ": " + s.count));

print("\n📊 Топ-5 отправителей по количеству доставок...");
const topSenders = db.deliveries.aggregate([
  {
    $lookup: {
      from: "users",
      localField: "sender_id",
      foreignField: "_id",
      as: "sender"
    }
  },
  { $unwind: "$sender" },
  {
    $group: {
      _id: { 
        user_id: "$sender_id", 
        name: { $concat: ["$sender.first_name", " ", "$sender.last_name"] } 
      },
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } },
  { $limit: 5 }
]).toArray();
print("✅ Топ отправителей:");
topSenders.forEach((s, i) => print("   " + (i+1) + ". " + s._id.name + ": " + s.count + " доставок"));

print("\n📊 Доставки за последнюю неделю с детальной информацией...");
const oneWeekAgo = new Date();
oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

const recentDeliveries = db.deliveries.aggregate([
  {
    $lookup: { from: "users", localField: "sender_id", foreignField: "_id", as: "sender" }
  },
  {
    $lookup: { from: "users", localField: "recipient_id", foreignField: "_id", as: "recipient" }
  },
  {
    $lookup: { from: "parcels", localField: "parcel_id", foreignField: "_id", as: "parcel" }
  },
  { $unwind: { path: "$sender", preserveNullAndEmptyArrays: true } },
  { $unwind: { path: "$recipient", preserveNullAndEmptyArrays: true } },
  { $unwind: { path: "$parcel", preserveNullAndEmptyArrays: true } },
  { $match: { created_at: { $gte: oneWeekAgo } } },
  {
    $project: {
      sender_name: { $concat: ["$sender.first_name", " ", "$sender.last_name"] },
      recipient_name: { $concat: ["$recipient.first_name", " ", "$recipient.last_name"] },
      tracking_number: "$parcel.tracking_number",
      weight_kg: "$parcel.weight_kg",
      status: 1,
      created_at: 1
    }
  }
]).toArray();
print("✅ Доставок за неделю: " + recentDeliveries.length);

// ----------------------------------------------------------------------------
// 7. ВАЛИДАЦИЯ И ОБРАБОТКА ОШИБОК
// ----------------------------------------------------------------------------
print("\n🔐 Проверка уникальности login (должна вызвать ошибку)...");
try {
  db.users.insertOne({
    _id: "550e8400-e29b-41d4-a716-4466554400aa",
    login: "new_user", // Дубликат!
    first_name: "Дубль",
    last_name: "Пользователь",
    email: "dup@example.com",
    password_hash: "$2b$12$hash",
    created_at: new Date(),
    updated_at: new Date()
  });
  print("❌ Ошибка: дубликат не обнаружен (индекс не работает?)");
} catch (e) {
  if (e.code === 11000) {
    print("✅ Ожидаемая ошибка дубликата: " + e.keyPattern.login + " уже существует");
  } else {
    print("❌ Неожиданная ошибка: " + e.message);
  }
}

print("\n🔐 Проверка уникальности email (должна вызвать ошибку)...");
try {
  db.users.insertOne({
    _id: "550e8400-e29b-41d4-a716-4466554400bb",
    login: "unique_login",
    first_name: "Ещё один",
    last_name: "Тест",
    email: "newuser@example.com", // Дубликат!
    password_hash: "$2b$12$hash",
    created_at: new Date(),
    updated_at: new Date()
  });
  print("❌ Ошибка: дубликат email не обнаружен");
} catch (e) {
  if (e.code === 11000) {
    print("✅ Ожидаемая ошибка дубликата email: " + e.keyValue.email);
  } else {
    print("❌ Неожиданная ошибка: " + e.message);
  }
}

// ----------------------------------------------------------------------------
// 8. ОПЕРАТОРЫ СРАВНЕНИЯ И ЛОГИКИ — демонстрация
// ----------------------------------------------------------------------------
print("\n🔍 Операторы сравнения: посылки с весом 1.0–3.0 кг...");
const weightRange = db.parcels.find({ 
  weight_kg: { $gte: 1.0, $lte: 3.0 } 
}).toArray();
print("✅ Найдено посылок в диапазоне: " + weightRange.length);

print("\n🔍 Логический оператор $or: пользователи Иван или Пётр...");
const orSearch = db.users.find({
  $or: [
    { first_name: "Иван" },
    { first_name: "Петр" }
  ]
}).toArray();
print("✅ Найдено пользователей: " + orSearch.length);

// ----------------------------------------------------------------------------
// 9. ПАГИНАЦИЯ
// ----------------------------------------------------------------------------
print("\n📄 Пагинация: пользователи, страница 1, лимит 2...");
const page = 1;
const limit = 2;
const paginated = db.users.find({})
  .skip((page - 1) * limit)
  .limit(limit)
  .toArray();
print("✅ Показано пользователей: " + paginated.length + " (стр. " + page + ")");
paginated.forEach((u, i) => print("   " + ((page-1)*limit + i + 1) + ". " + u.login));

// ----------------------------------------------------------------------------
// 10. ПОДСЧЁТЫ
// ----------------------------------------------------------------------------
print("\n🔢 Общее количество пользователей...");
const totalUsers = db.users.countDocuments({});
print("✅ Всего пользователей: " + totalUsers);

print("\n🔢 Агрегация: количество доставок по статусу...");
const deliveryCounts = db.deliveries.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } }
]).toArray();
deliveryCounts.forEach(d => print("   • " + d._id + ": " + d.count));

// ----------------------------------------------------------------------------
// 11. ФИНАЛЬНЫЙ ОТЧЁТ
// ----------------------------------------------------------------------------
print("\n" + "=".repeat(60));
print("📋 ИТОГОВЫЙ ОТЧЁТ");
print("=".repeat(60));
print("👥 Пользователей: " + db.users.countDocuments({}));
print("📦 Посылок: " + db.parcels.countDocuments({}));
print("🚚 Доставок: " + db.deliveries.countDocuments({}));
print("\n📊 Статусы доставок:");
db.deliveries.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
]).forEach(s => print("   • " + s._id.padEnd(12) + ": " + s.count));
print("=".repeat(60));
print("✅ Скрипт завершён успешно!\n");
