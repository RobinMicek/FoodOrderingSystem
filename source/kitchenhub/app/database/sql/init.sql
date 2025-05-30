/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

********************************************************
*/


-- 
-- TABLES
--


-- Table orders: Stores information about orders
CREATE TABLE `orders` (
  orderId INTEGER,
  establishmentId INTEGER,
  firstname TEXT,
  surname TEXT,
  email TEXT,
  phone TEXT,
  tag TEXT,
  totalPrice REAL,
  pickupTime TIMESTAMP,
  status TEXT DEFAULT 'CREATED',
  synced INTEGER DEFAULT 0,
  lastSync TIMESTAMP DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime'))
);


-- Table orders_products: Stores the relationship between orders and products
CREATE TABLE `orders_products` (
  orderId INTEGER,
  name TEXT,
  quantity INTEGER,
  orderPrice FLOAT DEFAULT 0,
  preparationTime TIMESTAMP
);


-- Table app_configuration: Stores variables that the app needs to function
CREATE TABLE `app_configuration` (
  serverUrl TEXT,
  establishmentToken TEXT,
  establishmentSlug TEXT,
  establishmentName TEXT,
  rabbitmqUrl TEXT,
  rabbitmqPort INT,
  rabbitmqUsername TEXT,
  rabbitmqPassword TEXT,
  pin TEXT,
  lastSync TIME,
  rabbitmqLastConnected TIMESTAMP
)