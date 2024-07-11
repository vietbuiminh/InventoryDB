import sqlite3
import os

conn = sqlite3.connect('database.db')
with open('schema.sql') as f:
  conn.executescript(f.read())

cur = conn.cursor()


def run_sql(sql, val):
  cur.execute(sql, val)
  conn.commit()


def get_id(sql, val):
  return int(cur.execute(sql, val).fetchone()[0])

def insert_media(href, comment):
  sql = "INSERT INTO media (href, comment) VALUES (?, ?)"
  val = (href, comment)
  run_sql(sql, val)

run_sql(
    "INSERT INTO categories (name, description, comment) VALUES (?,?,?)",
    ('hardware', 'Hardware related products', 'This is a hardware category'))
run_sql("INSERT INTO categories (name, description, comment) VALUES (?,?,?)",
        ('racking', 'Racking related products', 'This is a racking category'))
hardware_id = get_id("SELECT id FROM categories WHERE name = ?",
                     ('hardware', ))
racking_id = get_id("SELECT id FROM categories WHERE name = ?", ('racking', ))
run_sql(
    "INSERT INTO products (id_category, name, description, instock, comment, visible) VALUES (?,?,?,?,?,?)",
    (hardware_id, '8/3 bolt', 'Hardware related products', 1000,
     'This is a hardware category', 1))

for filename in os.listdir("static/img"):
    if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
        href = f"/static/img/{filename}"
        comment = "Image from static/img folder"
        insert_media(href, comment)

conn.close()
