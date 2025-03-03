import sqlite3
from datetime import datetime
connection = sqlite3.connect('fake_kfc.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, '
               'name VARCHAR(30), number VARCHAR(15), location VARCHAR(100), reg_date DATETIME);')
cursor.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, '
               'name VARCHAR(30), quantity INTEGER, price REAL, descr TEXT, photo VARCHAR(200), reg_date DATETIME);')
cursor.execute('''CREATE TABLE IF NOT EXISTS cart (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                cart_user INTEGER,
                cart_product INTEGER,
                quantity INTEGER,
                reg_date DATETIME,
                FOREIGN KEY (cart_user) REFERENCES user(id),
                FOREIGN KEY (cart_product) REFERENCES product(id));''')

connection.commit()
connection.close()


def get_product(pr_id):
    connection = sqlite3.connect('fake_kfc.db')
    cursor = connection.cursor()
    product = cursor.execute('''SELECT * 
                                    FROM products
                                    WHERE id = ?;''', (pr_id, )).fetchone()
    connection.close()
    return product


def check_regist(user_id):
    connection = sqlite3.connect('fake_kfc.db')
    cursor = connection.cursor()
    user = cursor.execute('''SELECT id FROM users WHERE id = ?;''', (user_id, )).fetchone()
    connection.close()
    if user:
        return True
    else:
        return False

def user_regist(name, user_phone, address):
    connection = sqlite3.connect('fake_kfc.db')
    cursor = connection.cursor()
    cursor.execute('''UPDATE users SET name = ?, number = ?, location = ?, reg_date = ?;''',
                   (name, user_phone, address, datetime.now()))
    connection.commit()
    connection.close()

connection.close()
