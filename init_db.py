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


for filename in os.listdir("static/img"):
    if filename.endswith((".jpg", ".jpeg", ".png", ".gif")):
        href = f"/img/{filename}"
        comment = "Image from static/img folder"
        insert_media(href, comment)

run_sql("INSERT INTO categories (name, description, comment) VALUES (?,?,?)",
        ('Racking', 'Racking related products', 'This is a racking category'))

hardware_id = get_id("SELECT id FROM categories WHERE name = ?",
                     ('Hardware', ))
racking_id = get_id("SELECT id FROM categories WHERE name = ?", ('Racking', ))
print(hardware_id, racking_id)

run_sql(
    "INSERT INTO products (id_category, id_media, name, description, instock, comment, visible) VALUES (?,?,?,?,?,?,?)",
    (hardware_id, 1, '8/3 nut', 'Hardware related products', 1000,
     'This is a hardware category', 1))
run_sql(
    "INSERT INTO products (id_category, id_media, name, description, instock, comment, visible) VALUES (?,?,?,?,?,?,?)",
    (hardware_id, 2, '8/3 bolt', 'Hardware related products', 500,
     'This is a hardware category', 1))
run_sql(
    "INSERT INTO products (id_category, id_media, name, description, instock, comment, visible) VALUES (?,?,?,?,?,?,?)",
    (hardware_id, 3, 'Spring Nut', 'Hardware related products', 800,
     'This is a hardware category', 1))
run_sql(
    "INSERT INTO products (id_category, id_media, name, description, instock, comment, visible) VALUES (?,?,?,?,?,?,?)",
    (hardware_id, 4, 'Washer', 'Hardware related products', 1200,
     'This is a hardware category', 1))
run_sql(
    "INSERT INTO products (id_category, id_media, name, description, instock, comment, visible) VALUES (?,?,?,?,?,?,?)",
    (int(racking_id), 5, '19ft Strut', 'Racking related products', 800,
     'This is a racking product', 1))
run_sql(
    "INSERT INTO products (id_category, id_media, name, description, instock, comment, visible) VALUES (?,?,?,?,?,?,?)",
    (int(hardware_id), 6, 'Split Ring', 'Hardware related products', 800,
     'This is a hardware product', 1))

run_sql("INSERT INTO groups (name,list) VALUES (?,?)",
        ('3/8" Hardware ', '2,3,6'))
run_sql("INSERT INTO groups (name,list) VALUES (?,?)",
        ('End Clamp (30mm)', ''))
run_sql("INSERT INTO groups (name,list) VALUES (?,?)", ('Mid Clamp ', ''))
run_sql("INSERT INTO groups (name,list) VALUES (?,?)",
        ('Bonded Mid Clamp ', ''))
run_sql("INSERT INTO groups (name,list) VALUES (?,?)",
        ('Ridge Brackets (twisted both sides)', ''))
run_sql("INSERT INTO groups (name,list) VALUES (?,?)",
        ('Ridge Brackets (straight, both sides)', ''))
run_sql("INSERT INTO groups (name,list) VALUES (?,?)",
        ('3/8" Hardware (ridge bracket centers)', ''))
run_sql("INSERT INTO groups (name,list) VALUES (?,?)",
        ('3/8" Hardware (long)', ''))
run_sql("INSERT INTO groups (name,list) VALUES (?,?)", ("Rail (19')*", '5'))
run_sql("INSERT INTO groups (name,list) VALUES (?,?)", ("Splice ", '5'))

conn.close()
