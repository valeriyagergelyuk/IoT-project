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
    logged_in = False
    if(rfid_id != vars.rfid_uid):
        profiles = fetch_all_profiles()
        for profile in profiles:
            if(rfid_uid == profile[1]):
                logged_in = True
                vars.rfid_uid = rfid_id
                vars.user_authenticated = True
                vars.user_id = profile[0]
                vars.temp_threshold = profile[2]
                vars.light_threshold = profile[3]
                vars.user_changed = True
                vars.email_user_auth = False
                return True
    else:
        logged_in = True
        return True
    
    if(logged_in == False):
        vars.user_valid = False
        return False
    

if __name__ == "__main__":
    profiles = fetch_all_profiles()
    for profile in profiles:
        print(f"UserID: {profile[0]}, RFID: {profile[1]}, Temp Threshold: {profile[2]}, Light Threshold: {profile[3]}")
