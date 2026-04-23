# MongoDB Queries для MeowMeowExpress

## Создание коллекций и индексов

### Создание индексов для коллекции users
```javascript
db.users.createIndex({ login: 1 }, { unique: true });
db.users.createIndex({ email: 1 }, { unique: true });
db.users.createIndex({ first_name: 1 });
db.users.createIndex({ last_name: 1 });
db.users.createIndex({ created_at: -1 });
```

### Создание индексов для коллекции parcels
```javascript
db.parcels.createIndex({ owner_id: 1 });
db.parcels.createIndex({ tracking_number: 1 }, { unique: true });
db.parcels.createIndex({ created_at: -1 });
```

### Создание индексов для коллекции deliveries
```javascript
db.deliveries.createIndex({ sender_id: 1 });
db.deliveries.createIndex({ recipient_id: 1 });
db.deliveries.createIndex({ parcel_id: 1 });
db.deliveries.createIndex({ status: 1, created_at: -1 });
```

---

## CREATE (Вставка документов)

### Вставка пользователя
```javascript
db.users.insertOne({
  login: "new_user",
  first_name: "Новый",
  last_name: "Пользователь",
  email: "newuser@example.com",
  password_hash: "$2b$12$hashed_password",
  created_at: new Date(),
  updated_at: new Date()
});
```

### Вставка нескольких пользователей
```javascript
db.users.insertMany([
  {
    login: "user1",
    first_name: "Иван",
    last_name: "Иванов",
    email: "user1@example.com",
    password_hash: "$2b$12$hash1",
    created_at: new Date(),
    updated_at: new Date()
  },
  {
    login: "user2",
    first_name: "Петр",
    last_name: "Петров",
    email: "user2@example.com",
    password_hash: "$2b$12$hash2",
    created_at: new Date(),
    updated_at: new Date()
  }
]);
```

### Вставка посылки
```javascript
db.parcels.insertOne({
  owner_id: ObjectId("507f1f77bcf86cd799439011"),
  tracking_number: "TRK123456789",
  description: "Новая посылка",
  weight_kg: 2.5,
  dimensions: "30x20x15 см",
  created_at: new Date(),
  updated_at: new Date()
});
```

### Вставка доставки
```javascript
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
```

---

## READ (Поиск документов)

### Получить пользователя по login
```javascript
db.users.findOne({ login: "ivanov_ivan" });
```

### Получить пользователя по email
```javascript
db.users.findOne({ email: "ivanov@example.com" });
```

### Получить пользователя по _id
```javascript
db.users.findOne({ _id: ObjectId("...") });
```

### Поиск пользователей по маске имени (используя $regex)
```javascript
db.users.find({ 
  first_name: { $regex: ".*анн.*", $options: "i" }
}).toArray();
```

### Поиск пользователей по маске фамилии
```javascript
db.users.find({ 
  last_name: { $regex: ".*ов.*", $options: "i" }
}).toArray();
```

### Поиск пользователей по маске имени и фамилии (AND)
```javascript
db.users.find({ 
  first_name: { $regex: ".*анн.*", $options: "i" },
  last_name: { $regex: ".*ов.*", $options: "i" }
}).toArray();
```

### Поиск пользователей по маске имени или фамилии (OR)
```javascript
db.users.find({ 
  $or: [
    { first_name: { $regex: ".*анн.*", $options: "i" } },
    { last_name: { $regex: ".*ов.*", $options: "i" } }
  ]
}).toArray();
```

### Получить посылки пользователя по owner_id
```javascript
db.parcels.find({ owner_id: ObjectId("...") }).toArray();
```

### Получить посылку по tracking_number
```javascript
db.parcels.findOne({ tracking_number: "TRK001A2B3C4D" });
```

### Получить доставки отправителя по sender_id
```javascript
db.deliveries.find({ sender_id: ObjectId("...") }).toArray();
```

### Получить доставки получателя по recipient_id
```javascript
db.deliveries.find({ recipient_id: ObjectId("...") }).toArray();
```

### Получить доставку по id
```javascript
db.deliveries.findOne({ _id: ObjectId("...") });
```

### Получить доставки по статусу
```javascript
db.deliveries.find({ status: "pending" }).toArray();
```

### Получить доставки по статусу с сортировкой
```javascript
db.deliveries.find({ status: "pending" }).sort({ created_at: -1 }).toArray();
```

### Получить доставки по диапазону дат
```javascript
db.deliveries.find({
  created_at: {
    $gte: new Date("2026-01-01"),
    $lt: new Date("2026-02-01")
  }
}).toArray();
```

### Получить доставки с конкретным набором статусов ($in)
```javascript
db.deliveries.find({
  status: { $in: ["pending", "in_transit"] }
}).toArray();
```

### Получить доставки с весом посылки больше определённого значения (с использованием $lookup)
```javascript
db.deliveries.aggregate([
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
```

---

## UPDATE (Обновление документов)

### Обновить пользователя по _id
```javascript
db.users.updateOne(
  { _id: ObjectId("...") },
  {
    $set: {
      first_name: "Иван",
      last_name: "Иванов",
      updated_at: new Date()
    }
  }
);
```

### Обновить статус доставки
```javascript
db.deliveries.updateOne(
  { _id: ObjectId("...") },
  {
    $set: {
      status: "delivered",
      actual_delivery_date: new Date(),
      updated_at: new Date()
    }
  }
);
```

### Увеличить вес посылки ($inc)
```javascript
db.parcels.updateOne(
  { _id: ObjectId("...") },
  { $inc: { weight_kg: 0.5 } }
);
```

### Добавить элемент в массив (если бы были массивы)
```javascript
db.users.updateOne(
  { _id: ObjectId("...") },
  { $push: { tags: "vip" } }
);
```

### Удалить элемент из массива
```javascript
db.users.updateOne(
  { _id: ObjectId("...") },
  { $pull: { tags: "temp" } }
);
```

### Добавить элемент в массив только если его там нет ($addToSet)
```javascript
db.users.updateOne(
  { _id: ObjectId("...") },
  { $addToSet: { tags: "vip" } }
);
```

### Обновить несколько документов ($set для всех)
```javascript
db.deliveries.updateMany(
  { status: "pending" },
  {
    $set: { status: "in_transit", updated_at: new Date() },
    $setOnInsert: { status_changed_at: new Date() }
  },
  { upsert: false }
);
```

---

## DELETE (Удаление документов)

### Удалить пользователя по _id
```javascript
db.users.deleteOne({ _id: ObjectId("...") });
```

### Удалить пользователя по login
```javascript
db.users.deleteOne({ login: "old_user" });
```

### Удалить все доставки со статусом "cancelled"
```javascript
db.deliveries.deleteMany({ status: "cancelled" });
```

### Удалить посылки старше определённой даты
```javascript
db.parcels.deleteMany({
  created_at: { $lt: new Date("2025-01-01") }
});
```

### Удалить все документы из коллекции
```javascript
db.users.deleteMany({});
```

---

## Агрегация

### Подсчёт количества посылок у каждого пользователя
```javascript
db.parcels.aggregate([
  { $group: { _id: "$owner_id", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
]).toArray();
```

### Получить список доставок с информацией о пользователе (с использованием $lookup)
```javascript
db.deliveries.aggregate([
  {
    $lookup: {
      from: "users",
      localField: "sender_id",
      foreignField: "_id",
      as: "sender"
    }
  },
  {
    $lookup: {
      from: "users",
      localField: "recipient_id",
      foreignField: "_id",
      as: "recipient"
    }
  },
  { $unwind: "$sender" },
  { $unwind: "$recipient" },
  {
    $project: {
      _id: 1,
      sender_name: { $concat: ["$sender.first_name", " ", "$sender.last_name"] },
      recipient_name: { $concat: ["$recipient.first_name", " ", "$recipient.last_name"] },
      status: 1,
      created_at: 1
    }
  }
]).toArray();
```

### Статистика доставок по статусу
```javascript
db.deliveries.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } },
  { $sort: { count: -1 } }
]).toArray();
```

### Средний вес посылок для каждого статуса доставки
```javascript
db.deliveries.aggregate([
  {
    $lookup: {
      from: "parcels",
      localField: "parcel_id",
      foreignField: "_id",
      as: "parcel"
    }
  },
  { $unwind: "$parcel" },
  {
    $group: {
      _id: "$status",
      avg_weight: { $avg: "$parcel.weight_kg" },
      total_count: { $sum: 1 }
    }
  }
]).toArray();
```

### Топ-5 пользователей по количеству отправленных доставок
```javascript
db.deliveries.aggregate([
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
      _id: { user_id: "$sender_id", name: { $concat: ["$sender.first_name", " ", "$sender.last_name"] } },
      count: { $sum: 1 }
    }
  },
  { $sort: { count: -1 } },
  { $limit: 5 }
]).toArray();
```

### Доставки за последнюю неделю с детальной информацией
```javascript
const oneWeekAgo = new Date();
oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

db.deliveries.aggregate([
  {
    $lookup: {
      from: "users",
      localField: "sender_id",
      foreignField: "_id",
      as: "sender"
    }
  },
  {
    $lookup: {
      from: "users",
      localField: "recipient_id",
      foreignField: "_id",
      as: "recipient"
    }
  },
  {
    $lookup: {
      from: "parcels",
      localField: "parcel_id",
      foreignField: "_id",
      as: "parcel"
    }
  },
  { $unwind: "$sender" },
  { $unwind: "$recipient" },
  { $unwind: "$parcel" },
  {
    $match: {
      created_at: { $gte: oneWeekAgo }
    }
  },
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
```

---

## Валидация данных

### Валидация вставки пользователя с обязательными полями
```javascript
db.users.insertOne({
  login: "test_user",
  first_name: "Тест",
  last_name: "Пользователь",
  email: "test@example.com",
  password_hash: "$2b$12$hash",
  created_at: new Date(),
  updated_at: new Date()
});
```

### Валидация вставки посылки с весом > 0
```javascript
db.parcels.insertOne({
  owner_id: ObjectId("..."),
  tracking_number: "TRK999",
  description: "Тестовая посылка",
  weight_kg: 1.0,
  dimensions: "10x10x10 см",
  created_at: new Date(),
  updated_at: new Date()
});
```

### Валидация уникальности login
```javascript
db.users.insertOne({
  login: "ivanov_ivan",
  first_name: "Дубль",
  last_name: "Иванов",
  email: "double@example.com",
  password_hash: "$2b$12$hash",
  created_at: new Date(),
  updated_at: new Date()
});
// Должна вызвать ошибку duplicate key
```

### Валидация уникальности email
```javascript
db.users.insertOne({
  login: "new_login",
  first_name: "Новый",
  last_name: "Пользователь",
  email: "ivanov@example.com",
  password_hash: "$2b$12$hash",
  created_at: new Date(),
  updated_at: new Date()
});
// Должна вызвать ошибку duplicate key
```

---

## Операторы сравнения

### Равенство ($eq)
```javascript
db.users.find({ login: { $eq: "ivanov_ivan" } }).toArray();
```

### Не равно ($ne)
```javascript
db.deliveries.find({ status: { $ne: "cancelled" } }).toArray();
```

### Больше ($gt)
```javascript
db.parcels.find({ weight_kg: { $gt: 2.0 } }).toArray();
```

### Меньше ($lt)
```javascript
db.parcels.find({ weight_kg: { $lt: 1.0 } }).toArray();
```

### Больше или равно ($gte)
```javascript
db.deliveries.find({ created_at: { $gte: new Date("2026-01-01") } }).toArray();
```

### Меньше или равно ($lte)
```javascript
db.deliveries.find({ created_at: { $lte: new Date("2026-01-31") } }).toArray();
```

### В списке ($in)
```javascript
db.deliveries.find({ status: { $in: ["pending", "in_transit"] } }).toArray();
```

### Не в списке ($nin)
```javascript
db.deliveries.find({ status: { $nin: ["cancelled", "delivered"] } }).toArray();
```

---

## Операторы логики

### AND (неявный, несколько условий)
```javascript
db.users.find({
  first_name: "Иван",
  last_name: "Иванов"
}).toArray();
```

### AND ($and)
```javascript
db.users.find({
  $and: [
    { first_name: "Иван" },
    { last_name: "Иванов" }
  ]
}).toArray();
```

### OR ($or)
```javascript
db.users.find({
  $or: [
    { first_name: "Иван" },
    { first_name: "Пётр" }
  ]
}).toArray();
```

---

## Операторы массива

### Добавить в массив ($push)
```javascript
db.users.updateOne(
  { _id: ObjectId("...") },
  { $push: { delivery_history: { delivery_id: ObjectId("..."), date: new Date() } } }
);
```

### Удалить из массива ($pull)
```javascript
db.users.updateOne(
  { _id: ObjectId("...") },
  { $pull: { delivery_history: { delivery_id: ObjectId("...") } } }
);
```

### Добавить только если нет ($addToSet)
```javascript
db.users.updateOne(
  { _id: ObjectId("...") },
  { $addToSet: { tags: "vip" } }
);
```

### Добавить элементы с сортировкой ($push + $each + $sort)
```javascript
db.users.updateOne(
  { _id: ObjectId("...") },
  {
    $push: {
      delivery_history: {
        $each: [{ delivery_id: ObjectId("..."), date: new Date() }],
        $sort: { date: -1 }
      }
    }
  }
);
```

---

## Операторы проекции

### Получить только определённые поля ($project)
```javascript
db.users.find({}, { login: 1, first_name: 1, last_name: 1, _id: 0 }).toArray();
```

### Исключить определённые поля
```javascript
db.users.find({}, { password_hash: 0, email: 0 }).toArray();
```

---

## Операторы сортировки

### Сортировка по возрастанию
```javascript
db.users.find({}).sort({ created_at: 1 }).toArray();
```

### Сортировка по убыванию
```javascript
db.users.find({}).sort({ created_at: -1 }).toArray();
```

### Сортировка по нескольким полям
```javascript
db.deliveries.find({}).sort({ status: 1, created_at: -1 }).toArray();
```

---

## Операторы пагинации

### Пагинация ($skip + $limit)
```javascript
db.users.find({}).skip(10).limit(10).toArray();
// Получить 11-20 пользователей
```

### С параметрами пагинации
```javascript
const page = 2;
const limit = 10;
db.users.find({}).skip((page - 1) * limit).limit(limit).toArray();
```

---

## Подсчёты

### Количество документов ($count)
```javascript
db.users.countDocuments({ login: "ivanov_ivan" });
```

### Агрегация с подсчётом
```javascript
db.users.aggregate([
  { $match: { first_name: "Иван" } },
  { $count: "total" }
]).toArray();
```

### Количество доставок по статусу
```javascript
db.deliveries.aggregate([
  { $group: { _id: "$status", count: { $sum: 1 } } }
]).toArray();
```

---

## Операторы времени

### Документы за сегодня
```javascript
const startOfDay = new Date();
startOfDay.setHours(0, 0, 0, 0);

db.deliveries.find({ created_at: { $gte: startOfDay } }).toArray();
```

### Документы за неделю
```javascript
const startOfWeek = new Date();
startOfWeek.setDate(startOfWeek.getDate() - 7);

db.deliveries.find({ created_at: { $gte: startOfWeek } }).toArray();
```

### Документы за месяц
```javascript
const startOfMonth = new Date();
startOfMonth.setMonth(startOfMonth.getMonth() - 1);

db.deliveries.find({ created_at: { $gte: startOfMonth } }).toArray();
```

---

## Операторы текстового поиска (если создан text index)

### Поиск по текстовому индексу
```javascript
db.users.createIndex({ first_name: "text", last_name: "text" });

db.users.find({ $text: { $search: "Иван Иванов" } }).toArray();
```

### Поиск с фразой
```javascript
db.users.find({ $text: { $search: "\"Иван Иванов\"" } }).toArray();
```

---

## Операторы регулярных выражений

### Поиск по началу строки
```javascript
db.users.find({ first_name: /^Иван/ }).toArray();
```

### Поиск по окончанию строки
```javascript
db.users.find({ last_name: /ов$/ }).toArray();
```

### Поиск по регулярному выражению с опциями
```javascript
db.users.find({ 
  email: { $regex: "@example\\.com$", $options: "i" }
}).toArray();
```

---

## Операторы специальных типов

### Поиск по диапазону чисел
```javascript
db.parcels.find({ weight_kg: { $gte: 0.5, $lte: 5.0 } }).toArray();
```

### Поиск по диапазону дат
```javascript
db.deliveries.find({
  created_at: { $gte: new Date("2026-01-01"), $lt: new Date("2026-02-01") }
}).toArray();
```

### Поиск по null
```javascript
db.deliveries.find({ actual_delivery_date: null }).toArray();
```

### Поиск по не-null
```javascript
db.deliveries.find({ actual_delivery_date: { $ne: null } }).toArray();
```

---

## Операторы модификации

### Возврат обновлённого документа
```javascript
db.deliveries.findOneAndUpdate(
  { _id: ObjectId("...") },
  { $set: { status: "delivered" } },
  { returnDocument: "after" }
);
```

### Удаление с возвратом
```javascript
db.deliveries.findOneAndDelete({ status: "cancelled" });
```

---

## Операторы с подзапросами

### Каскадное удаление на уровне приложения
```javascript
// 1. Удалить все посылки пользователя
db.parcels.deleteMany({ owner_id: ObjectId("...") });

// 2. Удалить все доставки, где пользователь отправитель или получатель
db.deliveries.deleteMany({
  $or: [
    { sender_id: ObjectId("...") },
    { recipient_id: ObjectId("...") }
  ]
});

// 3. Удалить самого пользователя
db.users.deleteOne({ _id: ObjectId("...") });
```

---

## Примеры из задания

### 1. Создание нового пользователя
```javascript
db.users.insertOne({
  login: "new_user",
  first_name: "Новый",
  last_name: "Пользователь",
  email: "newuser@example.com",
  password_hash: "$2b$12$hashed_password",
  created_at: new Date(),
  updated_at: new Date()
});
```

### 2. Поиск пользователя по логину
```javascript
db.users.findOne({ login: "ivanov_ivan" });
```

### 3. Поиск пользователя по маске имени и фамилии
```javascript
db.users.find({
  first_name: { $regex: ".*анн.*", $options: "i" },
  last_name: { $regex: ".*ов.*", $options: "i" }
}).toArray();
```

### 4. Создание посылки
```javascript
db.parcels.insertOne({
  owner_id: ObjectId("..."),
  tracking_number: "TRK123",
  description: "Описание",
  weight_kg: 1.5,
  dimensions: "10x10x10 см",
  created_at: new Date(),
  updated_at: new Date()
});
```

### 5. Получение посылок пользователя
```javascript
db.parcels.find({ owner_id: ObjectId("...") }).toArray();
```

### 6. Создание доставки от пользователя к пользователю
```javascript
db.deliveries.insertOne({
  sender_id: ObjectId("sender_id"),
  recipient_id: ObjectId("recipient_id"),
  parcel_id: ObjectId("parcel_id"),
  status: "pending",
  sender_address: "Адрес отправителя",
  recipient_address: "Адрес получателя",
  estimated_delivery_date: new Date("2026-01-20"),
  created_at: new Date(),
  updated_at: new Date()
});
```

### 7. Получение информации о доставке по получателю
```javascript
db.deliveries.find({ recipient_id: ObjectId("...") }).toArray();
```

### 8. Получение информации о доставке по отправителю
```javascript
db.deliveries.find({ sender_id: ObjectId("...") }).toArray();
```
