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
    print(vars.fan_on)
    data = {'IsFanMeantToBeOn': vars.fan_on, "Temperature": vars.temp, "Humidity": vars.hum}
    return jsonify(data)


@app.route('/get_email_and_light_data')
def return_current_lighting_values():
    data = {'LightAmount': vars.light_value, "isEmailSent": vars.email_sent, "emailBody": vars.email_body}
    return jsonify(data)

@app.route('/get_user')
def return_current_user_with_data():
    data = {'userID': vars.user_id, "userRFID": vars.rfid_uid, "isUserLoggedIn": vars.user_authenticated, "userTempThresh": vars.temp_threshold, "userLightThresh": vars.light_threshold, "correctUser": vars.user_valid}
    return jsonify(data)
    

if __name__ == "__main__":
    threading.Thread(target=dht_motor.loop, daemon=True).start()
    threading.Thread(target=light_sensor.loop, daemon=True).start()
    threading.Thread(target=rfid_scanner.loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
