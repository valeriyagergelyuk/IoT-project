from imports_variables import *
import imports_variables as vars
import verify_db as our_db
import time
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import paho.mqtt.subscribe as subscribe
import sqlite3

def send_email():
    """
    Function to send an email notification when a user enters.
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M")
    subject = "User Entered"
    body = f"User {vars.user_id} has entered at {formatted_time}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() 
            server.login(sender_email, sender_password)  
            server.send_message(msg) 
            print("User entered email sent successfully!")
            vars.email_user_auth = True 
            vars.user_changed = False  
    except Exception as e:
        print(f"Error sending email: {e}")

def update_thresholds(user_id, temp_threshold, light_threshold):
    """
    Function to update the temperature and light threshold values for an authenticated user in the database.
    """
    try:
        conn = sqlite3.connect('iot_project.db')
        cursor = conn.cursor()

        update_query = """
            UPDATE UserProfiles
            SET tempThreshold = ?, lightThreshold = ?
            WHERE userID = ?;
        """
        cursor.execute(update_query, (temp_threshold, light_threshold, user_id))
        
        conn.commit()
        print(f"Updated thresholds for User ID {user_id}: Temp Threshold={temp_threshold}, Light Threshold={light_threshold}")
        
    except sqlite3.Error as e:
        print(f"Error updating database: {e}")
    finally:
        conn.close()

def loop():
    """
    Main loop for reading RFID tags, checking database, and sending email if necessary.
    """
    global rfid_uid, user_authenticated, user_valid, temp_threshold, light_threshold, user_id

    while threads_active:
        msg = subscribe.simple("IoTlab/RFID", hostname="192.168.1.161")
        print(f"MQTT Message Received - Topic: {msg.topic}, Payload: {msg.payload}")

        tag_value = msg.payload.decode('utf-8')

        if tag_value:
            print(f"Scanned RFID Tag: {tag_value}")
            rfid_uid = tag_value

            try:
                conn = sqlite3.connect('iot_project.db')
                cursor = conn.cursor()
                cursor.execute("SELECT userID, tempThreshold, lightThreshold FROM UserProfiles WHERE rfidTag = ?", (tag_value,))
                result = cursor.fetchone()

                if result:
                    user_id, temp_threshold, light_threshold = result
                    user_authenticated = True
                    user_valid = True
                    vars.user_changed = True  # Indicate user context has changed
                    print(f"User authenticated: ID={user_id}, Temp Threshold={temp_threshold}, Light Threshold={light_threshold}")

                    if vars.email_user_auth is False and vars.user_changed:
                        send_email()

                    # Update thresholds with the current sensor values (from MQTT or sensors)
                    print(f"Updating thresholds with current values: Temp={vars.temp}, Light={vars.light}")
                    update_thresholds(user_id, vars.temp, vars.light)

                else:
                    user_authenticated = False
                    user_valid = False
                    vars.user_changed = False
                    print("Invalid RFID tag or user not registered.")

            except Exception as e:
                print(f"Error accessing database: {e}")
            finally:
                conn.close()

        time.sleep(1)
