import sqlite3
connection = sqlite3.connect("./SQL/student.db")
print(connection.getlimit)
cursor = connection.cursor()
print(cursor.arraysize)
for row in cursor.execute("SELECT name, email FROM students"):
    print(row)
