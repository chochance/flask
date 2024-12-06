import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
if rows:
    print("Users in database:", rows)
else:
    print("No users found.")
conn.close()

