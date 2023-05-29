# Connect to the database

import sqlite3 as db
connection = db.connect("framebot.db")
cursor = connection.cursor()

# Query the "show" table and print its contents
cursor.execute("SELECT * FROM show")
print("Contents of show table:")
for row in cursor.fetchall():
    print(row)

# Query the "bot" table and print its contents
cursor.execute("SELECT * FROM bot")
print("\nContents of bot table:")
for row in cursor.fetchall():
    print(row)

# Close the connection
connection.close()
