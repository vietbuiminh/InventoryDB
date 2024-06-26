DROP TABLE IF exists category;
DROP TABLE IF exists product;
DROP TABLE IF exists stock;

CREATE TABLE category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category_name VARCHAR(255)
);



CREATE TABLE product (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  category_id int,
  brand_name VARCHAR(255),
  product_name VARCHAR(255),
  product_description TEXT
);

DROP TABLE IF exists stock;

CREATE TABLE stock (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  product_id int,
  zone VARCHAR(10),
  level_number int,
  quantity int DEFAULT 0,
  attribute VARCHAR(255) DEFAULT 'N/A'
);