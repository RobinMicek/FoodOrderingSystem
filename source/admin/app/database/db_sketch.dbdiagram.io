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


// This is a structure of the db diagram
// Copy this text to dbdiagram.io to see the diagram 


Table products {
  productId INTEGER [primary key, increment]
  name VARCHAR(255)
  description TEXT
  price FLOAT
  preparationTime TIME
  imagePath VARCHAR(255)
  show TINYINT [default: 0]
}

Table orders {
  orderId INTEGER [primary key, increment]
  accountId INTEGER [ref: > accounts.accountId]
  establishmentId INTEGER [ref: > establishments.establishmentId]
  tag INT [default: NULL]
  createdTime TIMESTAMP [default: `CURRENT_TIMESTAMP`]
  pickupTime TIMESTAMP
  lastUpdate TIMESTAMP [default: `CURRENT_TIMESTAMP`]
  status VARCHAR(255) [default: 'CREATED']
  socketSent TINYINT [default: 0]
}

Table orders_products {
  orderId INTEGER [ref: > orders.orderId]
  productId INTEGER [ref: > products.productId]
  quantity INTEGER
  price FLOAT [default: 0]
}

Table accounts {
  accountId INTEGER [primary key, increment]
  email VARCHAR(255) [unique]
  phone VARCHAR(255)
  token VARCHAR(255)
  hash VARCHAR(255)
  firstname VARCHAR(255)
  surname VARCHAR(255)
  since TIMESTAMP [default: `CURRENT_TIMESTAMP`]
  dateOfBirth DATE
  active TINYINT [default: 1]
  role VARCHAR(255)
  lastTokenRefresh TIMESTAMP [default: `CURRENT_TIMESTAMP`]
}

Table menus {
  menuId INTEGER [primary key, increment]
  name VARCHAR(255)
  note TEXT
  description TEXT
  imagePath VARCHAR(255)
  show TINYINT [default: 0]
}

Table menus_products {
  menuId INTEGER [ref: > menus.menuId]
  productId INTEGER [ref: > products.productId]
}

Table establishments {
  establishmentId INTEGER [primary key, increment]
  name VARCHAR(255)
  imagePath VARCHAR(255)
  address VARCHAR(255)
  wifi TINYINT [default: 0]
  dineIn TINYINT [default: 0]
  yard TINYINT [default: 0]
  playground TINYINT [default: 0]
  parking TINYINT [default: 0]
  eCharger TINYINT [default: 0]
  show TINYINT [default: 0]
  slug VARCHAR(255)
  token VARCHAR(255)
}

Table establishments_menus {
  establishmentId INTEGER [ref: > establishments.establishmentId]
  menuId INTEGER [ref: > menus.menuId]
}

Table establishments_openinghours {
  establishmentId INTEGER [ref: > establishments.establishmentId]
  dayOfTheWeek INTEGER
  openingTime TIME
  closingTime TIME
}