import sqlite3
import os

dbPath = os.path.join('D:','\SPCC_BOT','DataBase', 'User.db')
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
login TEXT NOT NULL,
password TEXT NOT NULL)
''')

conn.commit()
conn.close()

print(f'База данных создана по пути: {dbPath}')