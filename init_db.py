import sqlite3

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


class Category:
    id = 0
    category_name = ""

    def __init__(self, category_name):
        self.id = id
        self.category_name = category_name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.category_name

    def create(self):
        if cur.connection.execute("SELECT * FROM category WHERE category_name = ?",
                                  (self.category_name, )).fetchone() == []:
            cur.connection.execute("INSERT INTO category (category_name) VALUES (?)",
                                   (self.category_name, ))
            self.id = cur.connection.execute(
                "SELECT id FROM category WHERE category_name = ?",
                (self.category_name, )).fetchone()[0]
            connection.commit()
            return True
        else:
            return False

    def delete(self):
        cur.connection.execute(
            "DELETE FROM category WHERE id = ?", (self.id, ))
        connection.commit()

    def __str__(self):
        return f"{self.id}. {self.category_name}"

    def __repr__(self):
        return f"<Category {self.category_name}>"


general_type = Category('general')
general_type.create()
print(general_type.get_name())
connection.commit()
connection.close()
