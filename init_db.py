import sqlite3

connection = sqlite3.connect('database.db')


class Category:
    id = 0
    category_name = ""

    def __init__(self, id, category_name):
        self.id = id
        self.category_name = category_name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.category_name

    def create(self, category_name):
        if None in connection.execute("SELECT * FROM category WHERE category_name = ?", (category_name,)).fetchone():
            connection.execute(
                "INSERT INTO category (category_name) VALUES (?)", (category_name,))
            self.category_name = category_name
            self.id = connection.execute(
                "SELECT id FROM category WHERE category_name = ?", (self.category_name,)).fetchone()[0]
            connection.commit()
            return True
        else:
            return False

    def __str__(self):
        return f"{self.id}. {self.category_name}"

    def __repr__(self):
        return f"<Category {self.category_name}>"


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO category (category_name) VALUES ('general')")
connection.commit()
connection.close()
