DROP TABLE IF exists categories;
DROP TABLE IF exists products;
DROP TABLE IF exists users;
DROP TABLE IF exists media;
DROP TABLE IF exists groups;

CREATE TABLE categories (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255),
  description TEXT NOT NULL DEFAULT '',
  comment TEXT DEFAULT NULL,
  datetime_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO categories (id, name, description, comment) VALUES (
  1,
  'Solar',
  'Solar products and PV technologies',
  'modules, panels, batteries, solar panels, solar roof, solar shade, etc.'
);
INSERT INTO categories (id, name, description, comment) VALUES (
  2,
  'Electrical',
  'Electrical products and equipment',
  'wiring, cables, power supplies, battery, etc.'
);
INSERT INTO categories (id, name, description, comment) VALUES (
  3,
  'Building',
  'Building products and equipment',
  'roof, shade, etc.'
);
INSERT INTO categories (id, name, description, comment) VALUES (
  4,
  'Hardware',
  'Hardware products and equipment',
  ''
);

CREATE TABLE products (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  id_category INTEGER NOT NULL DEFAULT 0,
  id_media INTEGER NOT NULL DEFAULT 0,
  name VARCHAR(255),
  brand VARCHAR(30),
  description TEXT NOT NULL DEFAULT '',
  instock INTEGER NOT NULL DEFAULT 0,
  comment TEXT NOT NULL DEFAULT '',
  visible INT(1) NOT NULL,
  datetime_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  perms INT(1) NOT NULL DEFAULT 0,
  first_name VARCHAR(255) NOT NULL DEFAULT '',
  last_name VARCHAR(255) NOT NULL DEFAULT '',
  email VARCHAR(255) NOT NULL DEFAULT '',
  password VARCHAR(255) NOT NULL DEFAULT '',
  secrete_question TEXT NOT NULL DEFAULT '',
  secrete_answer TEXT NOT NULL DEFAULT ''
);

CREATE TABLE media (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  href VARCHAR(255) NOT NULL DEFAULT '',
  comment TEXT NOT NULL DEFAULT ''
);

CREATE TABLE groups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name varchar(225) NOT NULL DEFAULT '',
  list varchar(255) NOT NULL default ''
);

INSERT INTO users (perms, first_name, last_name, email, password, secrete_question, secrete_answer) VALUES (1, 'admin', 'admin', 'admin@localhost', 'admin', 'What is your favorite color?', 'black');
