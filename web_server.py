from flask import Flask, render_template, request, jsonify
import RPi.GPIO as GPIO

app = Flask(__name__)

LED_PIN = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

@app.route("/") #This is the route you specify (in our case it is likely just / for now)
def home(): #When the route is called it would run this method
    return render_template('dashboard.html') #What the method runs

@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    data = request.json
    if data['state'] == 'ON':
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) #This part should be at the end at all times as anything under won't be ran

