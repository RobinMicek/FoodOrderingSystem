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


-- Table products: Stores information about products
  CREATE TABLE `products` (
    `productId` INTEGER PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255),
    `description` TEXT,
    `price` FLOAT,
    `preparationTime` TIME,
    `imagePath` VARCHAR(255),
    `show` TINYINT DEFAULT 0
  );



-- Table orders: Stores information about orders
CREATE TABLE `orders` (
  `orderId` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `accountId` INTEGER,
  `establishmentId` INTEGER,
  `tag` INTEGER DEFAULT NULL,
  `paymentType` VARCHAR(255) DEFAULT "CASH",
  `createdTime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `pickupTime` TIMESTAMP,
  `lastUpdate` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `status` VARCHAR(255) DEFAULT 'CREATED',
  `socketSent` TINYINT DEFAULT 0
);



-- Table orders_products: Stores the relationship between orders and products
CREATE TABLE `orders_products` (
  `orderId` INTEGER,
  `productId` INTEGER,
  `quantity` INTEGER,
  `price` FLOAT DEFAULT 0
);



-- Table accounts: Stores information about user accounts
CREATE TABLE `accounts` (
  `accountId` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `cardNumber` VARCHAR(255) UNIQUE,
  `email` VARCHAR(255) UNIQUE,
  `phone` VARCHAR(255),
  `token` VARCHAR(255),
  `hash` VARCHAR(255),
  `firstname` VARCHAR(255),
  `surname` VARCHAR(255),
  `walletBalance` INTEGER DEFAULT 0,
  `since` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `dateOfBirth` DATE,
  `active` TINYINT DEFAULT 1,
  `role` VARCHAR(255),
  `lastTokenRefresh` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Table accounts_wallet_refills: Stores information about user wallet refills
CREATE TABLE `accounts_wallet_refills` (
  `refillId` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `accountId` INTEGER,
  `amount` INTEGER,
  `establishmentId` INTEGER DEFAULT NULL,
  `date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



-- Table menus: Stores information about menus
CREATE TABLE `menus` (
  `menuId` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255),
  `note` TEXT,
  `description` TEXT,
  `imagePath` VARCHAR(255),
  `show` TINYINT DEFAULT 0
);



-- Table menus_products: Stores the relationship between menus and products
CREATE TABLE `menus_products` (
  `menuId` INTEGER,
  `productId` INTEGER
);



-- Table establishments: Stores information about establishments
CREATE TABLE `establishments` (
  `establishmentId` INTEGER PRIMARY KEY AUTO_INCREMENT,
  `name` VARCHAR(255),
  `imagePath` VARCHAR(255),
  `address` VARCHAR(255),
  `wifi` TINYINT DEFAULT 0,
  `dineIn` TINYINT DEFAULT 0,
  `yard` TINYINT DEFAULT 0,
  `playground` TINYINT DEFAULT 0,
  `parking` TINYINT DEFAULT 0,
  `eCharger` TINYINT DEFAULT 0,
  `show` TINYINT DEFAULT 0,
  `slug` VARCHAR(255),
  `token` VARCHAR(255)
);



-- Table establishments_menus: Stores the relationship between establishments and menus
CREATE TABLE `establishments_menus` (
  `establishmentId` INTEGER,
  `menuId` INTEGER
);



-- Table establishments_openinghours: Stores information about establishment opening hours
CREATE TABLE `establishments_openinghours` (
  `establishmentId` INTEGER,
  `dayOfTheWeek` INTEGER,
  `openingTime` TIME,
  `closingTime` TIME
);


-- Table stats_overall: Stores information about order statistics for each day - is generated automatically on a schedule
CREATE TABLE `stats_daily_overall` (
  `date` DATE PRIMARY KEY,
  `total_orders` INTEGER DEFAULT 0,
  `total_canceled_orders` INTEGER DEFAULT 0,
  `revenue_total` FLOAT DEFAULT 0,
  `revenue_cash` FLOAT DEFAULT 0,
  `revenue_wallet` FLOAT DEFAULT 0,
  `new_acc_created` INTEGER DEFAULT 0,
  `total_wallet_refills` INTEGER DEFAULT 0,
  `total_wallet_refills_amount` FLOAT DEFAULT 0,
  `average_order_price` FLOAT DEFAULT 0,
  `most_purchased_productId` INTEGER DEFAULT 0,
  `lastUpdate` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Table stats_overall: Stores information about order statistics for each day - is generated automatically on a schedule
CREATE TABLE `stats_daily_establishments` (
  `statsEstablishmentId` VARCHAR(255) PRIMARY KEY,
  `date` DATE NOT NULL,
  `establishmentId` INTEGER NOT NULL,
  `total_orders` INTEGER DEFAULT 0,
  `total_canceled_orders` INTEGER DEFAULT 0,
  `revenue_total` FLOAT DEFAULT 0,
  `revenue_cash` FLOAT DEFAULT 0,
  `revenue_wallet` FLOAT DEFAULT 0,
  `average_order_price` FLOAT DEFAULT 0,
  `most_purchased_productId` INTEGER DEFAULT 0,
  `lastUpdate` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)