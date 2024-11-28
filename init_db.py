import sqlite3

# Create and initialize the database
conn = sqlite3.connect('iot_project.db')
cursor = conn.cursor()

# Create table with default thresholds
cursor.execute('''
CREATE TABLE IF NOT EXISTS UserProfiles (
    userID TEXT PRIMARY KEY,
    rfidTag TEXT UNIQUE,
    tempThreshold REAL DEFAULT 25,
    lightThreshold REAL DEFAULT 400
)
''')

# Add users with RFID tags
users = [
    ('user1', '33a2130e', '21', '800'),
    ('user2', '1358daf7', '22', '600'),
    ('user3', '737a980e', '21', '1000'),
    ('Chris2', '0332d124', '24', '200')
]

for user in users:

    userID, rfidTag = user[0], user[1]
    tempThreshold = user[2] if len(user) > 2 else 25
    lightThreshold = user[3] if len(user) > 3 else 400

    cursor.execute('''
    INSERT OR IGNORE INTO UserProfiles (userID, rfidTag, tempThreshold, lightThreshold)
    VALUES (?, ?, ?, ?)
    ''', (userID, rfidTag, tempThreshold, lightThreshold))

# Commit changes and close
conn.commit()
conn.close()
print("Users added and database setup complete!")
