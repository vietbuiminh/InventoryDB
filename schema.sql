DROP TABLE IF exists category;
DROP TABLE IF exists product;
DROP TABLE IF exists stock;

CREATE TABLE category (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR(255),
  parent_id int(11) DEFAULT NULL,
  disable_footprints tinyint(1) NOT NULL DEFAULT 0,
  disable_manufacturers tinyint(1) NOT NULL DEFAULT 0,
  disable_autodatasheets tinyint(1) NOT NULL DEFAULT 0,
  disable_properties tinyint(1) NOT NULL DEFAULT 0,
  partname_regex text COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  partname_hint text COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  default_description text COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  default_comment text COLLATE utf8mb3_unicode_ci NOT NULL DEFAULT '',
  comment text COLLATE utf8mb3_unicode_ci DEFAULT NULL,
  datetime_added timestamp NOT NULL DEFAULT current_timestamp(),
  last_modified timestamp NOT NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

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