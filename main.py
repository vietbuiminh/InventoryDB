import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'SolarPodInventoryForKeepTracking'


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_categories_ls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT c.id AS id, c.name AS name, c.description AS description, c.comment AS comment, COUNT(p.id) AS products_count FROM categories c LEFT JOIN products p ON c.id = p.id_category GROUP BY c.id, c.name"
    )
    categories = cur.fetchall()
    conn.close()
    return categories


def get_product_info(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = ?", (id, ))
    product = cur.fetchone()
    conn.close()
    return product


def get_category(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM categories WHERE id = ?", (id, ))
    category = cur.fetchone()
    conn.close()
    return category


@app.route('/')
def index():
    conn = get_db_connection()
    categories = get_categories_ls()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html',
                           title="Home",
                           categories=categories,
                           products=products)


def add_product(id_category, name, description, instock, comment, visible):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (id_category, name, description, instock, comment, visible) VALUES (?,?,?,?,?,?)",
        (int(id_category), name, description, int(instock), comment,
         int(visible)))
    conn.commit()
    conn.close()


def add_category(name, description, comment):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO categories (name, description, comment) VALUES (?,?,?)",
        (name, description, comment))
    conn.commit()
    conn.close()


@app.route('/addcategory/', methods=('GET', 'POST'))
def addcategory():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        comment = request.form['comment']
        add_category(name, description, comment)
        flash('Category added')
        return redirect(url_for('index'))
    return render_template('addcategory.html',
                           title="Add Category",
                           categories=get_categories_ls())


@app.route('/addproduct/', methods=('GET', 'POST'))
def addproduct():
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        description = request.form['description']
        print(description)
        instock = int(request.form['instock'])
        print(instock)
        id_category = int(request.form['category'])
        print(id_category)
        comment = request.form['comment']
        print(comment)
        visible = int(request.form['visible'])
        print(visible)
        add_product(id_category, name, description, instock, comment, visible)
        print('new product added')
        return redirect(url_for('index'))
    return render_template('addproduct.html',
                           title="Add Product",
                           categories=get_categories_ls())


@app.route('/category/<int:id>/', methods=('GET', 'POST'))
def category(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id_category = ?", (id, ))
    products = cur.fetchall()
    conn.close()
    category_info = get_category(id)
    return render_template('category.html',
                           title=category_info['name'],
                           products=products,
                           category_info=category_info,
                           categories=get_categories_ls())


@app.route('/category/<int:id>/delete', methods=('POST', ))
def deleteCategory(id):
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id_category = ?", (int(id), ))
        cur.execute("DELETE FROM categories WHERE id = ?", (int(id), ))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))


@app.route('/productinfo/<int:id>/', methods=('GET', 'POST'))
def displayInfo(id):
    info = get_product_info(id)
    return render_template('info.html',
                           info=info,
                           categories=get_categories_ls())


@app.route('/productinfo/<int:id>/edit', methods=('GET', 'POST'))
def editProduct(id):
    info = get_product_info(id)
    return render_template('editproduct.html',
                           info=info,
                           categories=get_categories_ls())


@app.route('/productinfo/<int:id>/delete', methods=('POST', ))
def deleteProduct(id):
    if request.method == 'POST':
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM products WHERE id = ?", (int(id), ))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
