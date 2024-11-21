import sqlite3

def fetch_all_profiles():
    # Connect to the database
    conn = sqlite3.connect('iot_project.db')
    cursor = conn.cursor()

    # Fetch all user profiles
    cursor.execute('SELECT * FROM UserProfiles')
    profiles = cursor.fetchall()

    # Close the connection
    conn.close()
    return profiles

if __name__ == "__main__":
    profiles = fetch_all_profiles()
    for profile in profiles:
        print(f"UserID: {profile[0]}, RFID: {profile[1]}, Temp Threshold: {profile[2]}, Light Threshold: {profile[3]}")
