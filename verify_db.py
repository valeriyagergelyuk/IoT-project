from imports_variables import *
import imports_variables as vars
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

def check_user_rfid(rfid_id):
    if(rfid_id != vars.rfid_uid){
        profiles = fetch_all_profiles()
        for profile in profiles:
            if(rfid_uid == profile[1]):
                vars.rfid_uid = rfid_id
                vars.user_authenticated = True
                vars.temp_threshold = profile[2]
                vars.light_threshold = profile[3]
    }

if __name__ == "__main__":
    profiles = fetch_all_profiles()
    for profile in profiles:
        print(f"UserID: {profile[0]}, RFID: {profile[1]}, Temp Threshold: {profile[2]}, Light Threshold: {profile[3]}")
