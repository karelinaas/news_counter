import sqlite3

sqlite_connection = sqlite3.connect('db.db')
cursor = sqlite_connection.cursor()

cursor.execute('''CREATE TABLE updates (date text, delta integer)''')
cursor.execute('''CREATE TABLE last_titles (date text, title text)''')
cursor.execute('''CREATE TABLE proxies (proxy text)''')
sqlite_connection.commit()

cursor.close()
sqlite_connection.close()
