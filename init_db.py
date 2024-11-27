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

# Add a sample user
cursor.execute('''
INSERT OR IGNORE INTO UserProfiles (userID, rfidTag)
VALUES ('user1', '737a980e')
''')

# Commit changes and close
conn.commit()
conn.close()
print("Database setup complete!")
