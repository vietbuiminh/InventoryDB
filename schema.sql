DROP TABLE IF exists categories;
DROP TABLE IF exists product;
DROP TABLE IF exists stock;

CREATE TABLE categories (
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

INSERT INTO categories (name, parent_id, disable_footprints, disable_manufacturers, disable_autodatasheets, disable_properties, partname_regex, partname_hint, default_description, default_comment, comment, datetime_added, last_modified) VALUES
('Test', NULL, 0, 0, 0, 0, '', '', '', '', '', '2023-01-07 18:32:29', '2023-01-07 18:32:29');


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