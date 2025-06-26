import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
connection = sqlite3.connect("auditorium.db")

# Create a cursor object to interact with the database
cursor = connection.cursor()

# Commit the changes
connection.commit()


# Example: Fetch and display records
cursor.execute("SELECT * FROM shows")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * from seats")
rows = cursor.fetchall()
for row in rows:
    print(row)

cursor.execute("SELECT * FROM Bookings")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
connection.close()
