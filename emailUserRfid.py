from imports_variables import *
import imports_variables as vars

def send_email():
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

def update_thresholds():
    try:
        conn = sqlite3.connect('iot_project.db')
        cursor = conn.cursor()

        update_query = """
            UPDATE UserProfiles
            SET tempThreshold = ?, lightThreshold = ?
            WHERE userID = ?;
        """
        cursor.execute(update_query, (vars.temp_threshold, vars.light_threshold, vars.user_id))
        
        conn.commit()
        print(f"Updated thresholds for User ID {vars.user_id}: Temp Threshold={vars.temp_threshold}, Light Threshold={vars.light_threshold}")
        
    except sqlite3.Error as e:
        print(f"Error updating database: {e}")
    finally:
        conn.close()

def loop():
    while threads_active:
        msg = subscribe.simple("IoTlab/RFID", hostname = vars.hostname)
        print(f"MQTT Message Received - Topic: {msg.topic}, Payload: {msg.payload}")
        tag_value = msg.payload.decode('utf-8')

        if tag_value:
            print(f"Scanned RFID Tag: {tag_value}")
            vars.rfid_uid = tag_value

            try:
                conn = sqlite3.connect('iot_project.db')
                cursor = conn.cursor()
                cursor.execute("SELECT userID, tempThreshold, lightThreshold FROM UserProfiles WHERE rfidTag = ?", (tag_value,))
                result = cursor.fetchone()

                if result:
                    vars.user_id, vars.temp_threshold, vars.light_threshold = result
                    vars.user_authenticated = True
                    vars.user_valid = True
                    vars.user_changed = True  # Indicate user context has changed
                    print(f"User authenticated: ID={vars.user_id}, Temp Threshold={vars.temp_threshold}, Light Threshold={vars.light_threshold}")

                    if vars.email_user_auth is False and vars.user_changed:
                        send_email()

                    # Update thresholds with the current sensor values (from MQTT or sensors)
                    print(f"Updating thresholds with current values: Temp={vars.temp_threshold}, Light={vars.light_threshold}")
                    update_thresholds()
                    publish.single("IoTlab/lightChange", payload=vars.light_threshold, hostname=vars.hostname)

                else:
                    vars.user_authenticated = False
                    vars.user_valid = False
                    vars.user_changed = False
                    print("Invalid RFID tag or user not registered.")

            except Exception as e:
                print(f"Error accessing database: {e}")
            finally:
                conn.close()

        time.sleep(1)
