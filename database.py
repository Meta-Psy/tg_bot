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


