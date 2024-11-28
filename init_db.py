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
    ('user1', '33a2130e'),
    ('user2', '1358daf7'),
    ('user3', '737a980e')
]

for userID, rfidTag in users:
    cursor.execute('''
    INSERT OR IGNORE INTO UserProfiles (userID, rfidTag)
    VALUES (?, ?)
    ''', (userID, rfidTag))

# Commit changes and close
conn.commit()
conn.close()
print("Users added and database setup complete!")
