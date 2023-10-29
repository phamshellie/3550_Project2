import sqlite3

#connection to the database
conn = sqlite3.connect('totally_not_my_privateKeys.db')

#cursor object
cursor = conn.cursor()

#command to create the table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS keys(
        kid INTEGER PRIMARY KEY AUTOINCREMENT,
        key BLOB NOT NULL,
        exp INTEGER NOT NULL
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()

print("Database and table created successfully.")
