import sqlite3
import re
from flask import Flask, render_template, request, url_for, flash, redirect, abort, session, get_flashed_messages
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from processtext import processPasteBOM
import numpy as np
from thefuzz import fuzz

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'SolarPodInventoryForKeepTracking'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?',
                        (user_id, )).fetchone()
    conn.close()
    if user is None:
        abort(404)
    else:
        return User(user['id'], user['perms'], user['first_name'],
                    user['last_name'], user['email'], user['password'],
                    user['secrete_question'], user['secrete_answer'])


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_group_ls():
    id_ls = []
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, list FROM groups ORDER BY name")
    group_ls = cur.fetchall()
    try:
        for group in group_ls:
            product_ls = [int(ele) for ele in group['list'].split(',')]
            print(product_ls)
            id_ls.append(product_ls)
    except Exception as e:
        print(e)
        print('List has no elements or not an integer list')
        if group_ls[0] == '':
            id_ls.append([])
    conn.close()
    return group_ls, id_ls


def get_categories_ls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT c.id AS id, c.name AS name, c.description AS description, c.comment AS comment, COUNT(p.id) AS products_count FROM categories c LEFT JOIN products p ON c.id = p.id_category GROUP BY c.id, c.name"
    )
    categories = cur.fetchall()
    conn.close()
    return categories


def get_product_ls():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT p.id AS id, p.name AS name, p.description AS description, p.instock AS instock, p.comment AS comment, p.visible AS visible, p.last_modified AS last_modified, c.id AS id_category, c.name AS name_category, c.description AS description_category, c.comment AS comment_category, m.href AS link FROM products p LEFT JOIN categories c ON p.id_category = c.id LEFT JOIN media m ON p.id_media = m.id"
    )
    products = cur.fetchall()
    conn.close()
    return products


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


def retrieveALLUsers():
    conn = get_db_connection()
    cursor = conn.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users


def retrieveUser(id):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM coaches WHERE id = ?",
                        (id, )).fetchone()
    conn.close()
    if user is None:
        abort(404)
    return user


@app.route('/')
def index():
    flash("Test1", 'primary')
    get_flashed_messages()
    conn = get_db_connection()
    categories = get_categories_ls()
    products = get_product_ls()
    groups, groups_id_ls = get_group_ls()
    conn.close()
    return render_template('index.html',
                           title="Home",
                           categories=categories,
                           products=products,
                           groups=groups,
                           groups_id_ls=groups_id_ls)


def add_product(id_category, name, description, instock, comment, visible):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (id_category, id_media, name, description, instock, comment, visible) VALUES (?,?,?,?,?,?,?)",
        (int(id_category), 6, name, description, int(instock), comment,
         int(visible)))
    conn.commit()
    conn.close()


def delete_product(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id = ?", (id, ))
    conn.commit()


def delete_category(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM categories WHERE id = ?", (id, ))
    conn.commit()


def add_category(name, description, comment):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO categories (name, description, comment) VALUES (?,?,?)",
        (name, description, comment))
    conn.commit()
    conn.close()


def checkExisting(email, password, users):
    for user in users:
        if user['email'] == email:
            if user['password'] == password:
                return True, user['id']
        else:
            return False, 0
    return False, 0


def checkValidEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False


def checkExistingEmail(email, users):
    for user in users:
        if user['email'] == email:
            return True
    return False


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    users = retrieveALLUsers()
    try:
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            print(email, password)
            users = retrieveALLUsers()
            checkBool, id = checkExisting(email, password, users)
            if (checkBool is False):
                pass
            # if True:
            # flash('Wrong password or username', 'error')
            else:
                user = load_user(id)
                login_user(user, remember=True)
                print("Sucessful to login")
                return redirect(url_for('index'))

        return render_template('login.html',
                               title="Login",
                               categories=get_categories_ls())
    except Exception as e:
        # flash(e, 'error')
        print('Error', e)
        return render_template('login.html',
                               title="Login",
                               categories=get_categories_ls())


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


@app.route('/addproject/')
def addproject():
    return render_template('addproject.html',
                           title="Add Project",
                           products=get_product_ls(),
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


def get_instock_product(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id = ?", (id, ))
    product = cur.fetchone()
    conn.close()
    return int(product['instock'])


def bom_update_product(id, subtract):
    if get_instock_product(id) < subtract:
        return False
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE products SET instock = instock - ? WHERE id = ?",
                    (subtract, id))
        conn.commit()
        return True


@app.route('/addproject/previewproject/', methods=('POST', 'GET'))
def previewproject():
    get_flashed_messages()
    groups, groups_id_ls = get_group_ls()
    text = request.args.get('text')
    df = processPasteBOM(text)
    ls_recognize = []
    recognize_group_id = []
    qty_ls = []
    for index, row in df.iterrows():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM groups WHERE name LIKE ?",
                    (row['Bill of Materials'], ))
        recognize_id = cur.fetchone()
        conn.close()
        if recognize_id != None:
            ls_recognize.append(index)
            recognize_group_id.append(recognize_id[0])
            qty_ls.append(row['qty'])
    if request.method == 'POST':
        for index, id in enumerate(recognize_group_id):
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT list FROM groups WHERE id = ?", (id, ))
            list_id = cur.fetchone()
            product_ls = [int(ele) for ele in list_id[0].split(',')]
            for product_id in product_ls:
                check = bom_update_product(product_id, int(qty_ls[index]))
                if check == False:
                    flash(
                        'Please update inventory stock, not enough to update for BOM',
                        'danger')
                    return redirect(url_for('index'))

            flash('BOM updated successfully', 'success')
            print(product_ls)
            conn.close()
        return redirect(url_for('index'))
    return render_template('previewproject.html',
                           title="Preview BOM",
                           products=get_product_ls(),
                           groups=groups,
                           groups_id_ls=groups_id_ls,
                           data=df,
                           ls_recognize=ls_recognize,
                           categories=get_categories_ls())


@app.route('/textprocessbom/', methods=('POST', 'GET'))
def textprocessbom():
    text = request.form['pastetext']
    return redirect(url_for('previewproject', text=text))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
