Table products {
  product_id INTEGER
  name STRING
  description STRING
  price FLOAT
  menu_id INTEGER
  image_path STRING
  preparation_time INTEGER
  show BOOLEAN
}

Table orders {
  order_id INTEGER
  account_id INTEGER
  tag INTEGER
  pickup_time DATE
  status STRING
}

Table orders_products {
  order_id INTEGER
  product_id INTEGER
  price FLOAT
}

Table accounts {
  account_id INTEGER
  hash STRING
  firstname STRING
  surname STRING
  date_of_birth DATE
  email STRING
  active BOOLEAN
  role STRING
}

Table menus {
  menu_id INTEGER
  name STRING
  note STRING
  description STRING
  image_path STRING
  show BOOLEAN
}

Table establishments {
  establishment_id INTEGER
  name INTEGER
  image_path STRING

  address STRING

  wifi BOOLEAN
  dine_in BOOLEAN
  yard BOOLEAN
  playground BOOLEAN
  parking BOOLEAN
  e_charger BOOLEAN

  show BOOLEAN
}

Table establishments_menus {
  establishment_id INTEGER
  menu_id INTEGER
}

Table establishments_openinghours {
  establishment_id INTEGER

  monday_opening_time FLOAT
  monday_closing_time FLOAT
  tuesday_opening_time FLOAT
  tuesday_closing_time FLOAT
  wednesday_opening_time FLOAT
  wednesday_closing_time FLOAT
  thursday_opening_time FLOAT
  thursday_closing_time FLOAT
  friday_opening_time FLOAT
  friday_closing_time FLOAT
  saturday_opening_time FLOAT
  saturday_closing_time FLOAT
  sunday_opening_time FLOAT
  sunday_closing_time FLOAT
}

Table newsletters {
  newsletter_id INTEGER
  image_path STRING
  heading STRING
  body STRING
}

Ref: establishments.establishment_id > establishments_menus.establishment_id
Ref: menus.menu_id > establishments_menus.menu_id
Ref: establishments.establishment_id > establishments_openinghours.establishment_id

Ref: orders.order_id > orders_products.order_id
Ref: products.product_id > orders_products.product_id

Ref: accounts.account_id > orders.account_id
Ref: menus.menu_id > products.menu_id