from flask import Flask, request, jsonify, render_template
import atexit
import sqlite3
import threading
import RPi.GPIO as GPIO
from imports_variables import *
import imports_variables as vars
import emailTemperature as dht_motor
import emailLight as light_sensor
import emailUserRfid as rfid_scanner

app = Flask(__name__)


def clean_up_before_exit():
    print(" Cleaning...")
    GPIO.cleanup()


atexit.register(clean_up_before_exit)


# def check_user_rfid(rfid_uid):
#     conn = sqlite3.connect('iot_project.db')
#     cursor = conn.cursor()
#     cursor.execute('SELECT * FROM UserProfiles WHERE rfidTag = ?', (rfid_uid,))
#     user = cursor.fetchone()
#     conn.close()
#     return user

# def assign_rfid_to_user(user_id, rfid_tag, temp_thresh, light_thresh):
#     conn = sqlite3.connect('iot_project.db')
#     cursor = conn.cursor()
#     try:
#         cursor.execute('''
#         INSERT INTO UserProfiles (userID, rfidTag, tempThreshold, lightThreshold)
#         VALUES (?, ?, ?, ?)
#         ''', (user_id, rfid_tag, temp_thresh, light_thresh))
#         conn.commit()
#         return True
#     except sqlite3.IntegrityError:
#         return False
#     finally:
#         conn.close()


@app.route("/") 
def home(): 
    return render_template('dashboard.html', data={'temperature': vars.temp, 'humidity': vars.hum}) 

@app.route("/editPreferences")
def edit_screen():
    return render_template('editPref.html', data={'temperature': vars.temp, 'humidity': vars.hum}) 


@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    data = request.json
    if data['state'] == 'ON':
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    return jsonify(success=True)


@app.route('/get_temp_data')
def return_current_dht_values():
    data = {'IsFanMeantToBeOn': vars.fan_on, "Temperature": vars.temp, "Humidity": vars.hum}
    return jsonify(data)


@app.route('/get_email_and_light_data')
def return_current_lighting_values():
    data = {'LightAmount': vars.light_value, "isEmailSent": vars.email_sent, "emailBody": vars.email_body}
    return jsonify(data)


# @app.route('/get_user_profile', methods=['GET'])
# def get_user_profile():
#     global user_id, rfid_uid, user_authenticated, temp_threshold, light_threshold

#     if user_authenticated:
#         return jsonify({
#             "userID": user_id,
#             "userRFID": rfid_uid,
#             "isUserLoggedIn": user_authenticated,
#             "userTempThresh": temp_threshold,
#             "userLightThresh": light_threshold
#         })
#     else:
#         return jsonify({
#             "userID": None,
#             "userRFID": None,
#             "isUserLoggedIn": False,
#             "userTempThresh": None,
#             "userLightThresh": None
#         })


# @app.route('/assign_rfid', methods=['POST'])
# def assign_rfid():
#     data = request.json
#     user_id = data.get('userID')
#     rfid_tag = data.get('rfidTag')

#     # Fetch the user's existing threshold values from the database
#     try:
#         conn = sqlite3.connect('iot_project.db')
#         cursor = conn.cursor()

#         # Fetch the thresholds for the user from the database
#         cursor.execute('SELECT tempThreshold, lightThreshold FROM UserProfiles WHERE userID = ?', (user_id,))
#         result = cursor.fetchone()

#         if result:
#             # If thresholds are found for the user, assign them
#             temp_thresh, light_thresh = result
#         else:
#             # If no thresholds are found, return an error message
#             return jsonify({'success': False, 'message': 'User not found in the database!'})

#         # Insert the RFID and associated thresholds into the database
#         cursor.execute('INSERT INTO UserProfiles (userID, rfidTag, tempThreshold, lightThreshold) VALUES (?, ?, ?, ?)',
#                        (user_id, rfid_tag, temp_thresh, light_thresh))
#         conn.commit()

#         print(f"Assigned RFID {rfid_tag} to user {user_id} with thresholds: tempThreshold={temp_thresh}, lightThreshold={light_thresh}.")
#         return jsonify({'success': True, 'message': 'RFID tag assigned successfully!'})

#     except sqlite3.IntegrityError as e:
#         print(f"Error assigning RFID: {e}")
#         return jsonify({'success': False, 'message': 'RFID tag already assigned!'})
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         return jsonify({'success': False, 'message': 'An error occurred while assigning the RFID tag.'})
#     finally:
#         conn.close()


if __name__ == "__main__":
    threading.Thread(target=dht_motor.loop, daemon=True).start()
    threading.Thread(target=light_sensor.loop, daemon=True).start()
    threading.Thread(target=rfid_scanner.loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
