from imports_variables import *
import imports_variables as vars
import emailTemperature as dht_motor
import emailLight as light_sensor
import emailUserRfid as rfid_scanner

app = Flask(__name__)

def clean_up_before_exit():
    print(" Cleaning...")
    GPIO.cleanup()

# Activates the function to be called when shutdown
atexit.register(clean_up_before_exit)

# Loads the webpage
@app.route("/") 
def home(): 
    return render_template('dashboard.html', data={'temperature': temp, 'humidity': hum}) 
@app.route("/editPreferences")
def editScreen():
    return render_template('editPref.html', data={'temperature': temp, 'humidity': hum}) 

# Toggles the led on the breadboard when the image changes
@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    data = request.json
    if data['state'] == 'ON':
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    return jsonify(success=True)

# Gets information on fan state, temperature and humditiy to display on the webpage
@app.route('/get_temp_data')
def returnCurrentDhtRelatedValues():
    data = {'IsFanMeantToBeOn': vars.fan_on, "Temperature": vars.temp, "Humidity": vars.hum}
    return jsonify(data)

@app.route('/get_email_and_light_data')
def returnCurrentLightingRelatedValues():
    data = {'LightAmount': vars.light_value, "isEmailSent": vars.email_sent, "emailBody": vars.email_body}
    return jsonify(data)

@app.route('/get_user_profile')
def returnUserProfileValues():
    data = {'userID': vars.user_id, 'userRFID': vars.rfid_uid, 'isUserLoggedIn':vars.user_authenticated, 'isLoginFailed': vars.user_valid, 'userTempThresh': vars.temp_threshold, 'userLightThresh': vars.light_threshold}
    return jsonify(data)

if __name__ == "__main__":
    threading.Thread(target=dht_motor.loop, daemon=True).start()
    threading.Thread(target=light_sensor.loop, daemon=True).start()
    threading.Thread(target=rfid_scanner.loop, daemon=True).start()
    app.run(host='0.0.0.0', port=5000) 

    
