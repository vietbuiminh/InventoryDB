import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

category_id = cur.execute("SELECT id FROM category").fetchall()
print(category_id)
connection.commit()
connection.close()
