import sqlite3

connection = sqlite3.connect('fake_kfc.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS users ('
               'id INTEGER, '
               'name TEXT, '
               'number TEXT'
               ');')
connection.commit()
id = 3
name = "Alex"
number = 933977109
cursor.execute('INSERT INTO users (id, name, number) VALUES (?, ?, ?);', (id, name, number))
connection.commit()
info = cursor.execute('SELECT name FROM users WHERE id > ?', (1, )).fetchall()
print(info)
cursor.execute('UPDATE users SET name = ? WHERE id = ?;', ("Alex", 1))
connection.commit()
cursor.execute('DELETE FROM users WHERE id > ?;', (1, ))
connection.commit()

connection.close()
