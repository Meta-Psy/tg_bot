import sqlite3
from datetime import datetime

conn = sqlite3.connect(database='kfc.db')
cursor = conn.cursor()


cursor.execute('CREATE TABLE IF NOT EXISTS users ('
               'id INTEGER PRIMARY KEY AUTOINCREMENT, '
               'tg_id INTEGER, '
               'name VARCHAR(30), '
               'number VARCHAR (15), '
               'location VARCHAR (100), '
               'reg_date DATETIME'
               ');')
cursor.execute('CREATE TABLE IF NOT EXISTS food ('
               'id INTEGER PRIMARY KEY AUTOINCREMENT, '
               'name VARCHAR(50), '
               'descr TEXT, '
               'price REAL, '
               'photo VARCHAR(100), '
               'quantity INTEGER'
               ');')
cursor.execute('CREATE TABLE IF NOT EXISTS cart ('
               'id INTEGER PRIMARY KEY AUTOINCREMENT, '
               'user_id INTEGER, '
               'pr_id INTEGER, '
               'quantity INTEGER, '
               'total_price REAL'
               ');')

# cursor.execute('INSERT INTO food (name, descr, price, photo, quantity) VALUES '
#                '("Бургер", "Сочный бургер", 45000, '
#                '"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSj9YK1kXl9d0umCSzj_1xeESlWg1G_9cSiDw&s",'
#                '10)')
#
# cursor.execute('INSERT INTO food (name, descr, price, photo, quantity) VALUES '
#                '("Пицца", "Классическая пицца с сыром и томатным соусом", 75000, '
#                '"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpizzurlEX", 20)')
#
# cursor.execute('INSERT INTO food (name, descr, price, photo, quantity) VALUES '
#                '("Суши", "Ассорти из свежих суши с васаби и имбирем", 65000, '
#                '"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSushiURL", 15)')
#
# cursor.execute('INSERT INTO food (name, descr, price, photo, quantity) VALUES '
#                '("Паста", "Итальянская паста с соусом болоньезе", 70000, '
#                '"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcPastaURL", 10)')
#
# cursor.execute('INSERT INTO food (name, descr, price, photo, quantity) VALUES '
#                '("Салат Цезарь", "Свежий салат с курицей, пармезаном и соусом Цезарь", 50000, '
#                '"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcCaesarURL", 30)')
#
# cursor.execute('INSERT INTO food (name, descr, price, photo, quantity) VALUES '
#                '("Лимонад", "Освежающий лимонад с натуральными ингредиентами", 30000, '
#                '"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcLemonadeURL", 50)')

conn.commit()
conn.close()


def registration_db(tg_id, name, number, location):
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (tg_id, name, number, location, reg_date) VALUES (?, ?, ?, ?, ?);',
                   (tg_id, name, number, location, datetime.now()))
    conn.commit()
    conn.close()
    return True


def check_db(tg_id):
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    user = cursor.execute('SELECT tg_id FROM users WHERE tg_id = ?;', (tg_id, )).fetchone()
    conn.close()
    if user:
        return True
    else:
        return False


def get_products():
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    products = cursor.execute('SELECT id, name, quantity FROM food WHERE quantity > 0').fetchall()
    conn.close()
    return products


def get_product(prod_id):
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    product = cursor.execute('SELECT * FROM food WHERE id = ?', (prod_id, )).fetchone()
    conn.close()
    return product


def add_to_cart_db(user_id, pr_id, quantity, total_price):
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cart (user_id, pr_id, quantity, total_price) VALUES (?, ?, ?, ?)',
                   (user_id, pr_id, quantity, total_price))
    conn.commit()
    conn.close()


def get_prod_cart(user_id):
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    cart = cursor.execute('SELECT pr_id, quantity, total_price FROM cart WHERE user_id=?',
                          (user_id, )).fetchall()
    conn.close()
    return cart

def get_product_cart(user_id, pr_id):
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    product = cursor.execute('SELECT quantity FROM cart WHERE user_id=? AND pr_id=?',
                             (user_id, pr_id)).fetchone()
    conn.close()
    return product

def update_product_cart(quantity, user_id, pr_id):
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE cart SET quantity=? WHERE user_id=? AND pr_id=?', (quantity, user_id, pr_id))
    conn.commit()
    conn.close()

def del_prod_cart(user_id, prod_id):
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart WHERE user_id=? AND pr_id=?',
                   (user_id, prod_id))
    conn.commit()
    conn.close()

def clear_cart(user_id):
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cart WHERE user_id=?', (user_id, ))
    conn.commit()
    conn.close()

def change_product(quantity, pr_id):
    conn = sqlite3.connect(database='kfc.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE food SET quantity=? WHERE id=?', (quantity, pr_id))
    conn.commit()
    conn.close()
