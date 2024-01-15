/*
********************************************************

    Tento kód je součástí projektu 'K Okénku',
    který je psán jako maturitní práce z informatiky.

    Gymnázium Sokolov a Krajské vzdělávací centrum,
    příspěvková organizace

    Robin Míček, 8.E

    Jakákoliv úprava a distribuce tohoto kódu 
    bez povolení autora je zakázána!

    © Robin Míček 2023 - 2024

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
  `tag` INT DEFAULT NULL,
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
  `email` VARCHAR(255) UNIQUE,
  `phone` VARCHAR(255),
  `token` VARCHAR(255),
  `hash` VARCHAR(255),
  `firstname` VARCHAR(255),
  `surname` VARCHAR(255),
  `since` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  `dateOfBirth` DATE,
  `active` TINYINT DEFAULT 1,
  `role` VARCHAR(255),
  `lastTokenRefresh` TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
)