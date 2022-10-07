import sqlite3

conn = sqlite3.connect("filename")
db = conn.cursor()
db.execute('CREATE TABLE filename(id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT, text TEXT)')
conn.close()
