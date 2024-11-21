import sqlite3

def initialize_database():
    conn = sqlite3.connect('iot_project.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserProfiles (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            RFIDTagNumber TEXT NOT NULL UNIQUE,
            TemperatureThreshold REAL NOT NULL,
            LightIntensityThreshold REAL NOT NULL
        )
    ''')

    cursor.execute('''
        INSERT INTO UserProfiles (RFIDTagNumber, TemperatureThreshold, LightIntensityThreshold)
        VALUES 
        ('33 A2 13 0E', 25.0, 300.0),
        ('12 B3 45 6F', 22.5, 350.0),
        ('89 D4 56 7A', 28.0, 400.0)
    ''')

    conn.commit()
    conn.close()
    print("New database initialized successfully with the updated schema!")

if __name__ == "__main__":
    initialize_database()
