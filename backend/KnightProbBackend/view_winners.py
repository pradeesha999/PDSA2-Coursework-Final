import sqlite3

conn = sqlite3.connect('../../database/knightstour.db')  # adjust if needed
cursor = conn.cursor()

cursor.execute("SELECT * FROM winners")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
