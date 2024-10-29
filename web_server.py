from flask import Flask, render_template, request, jsonify
from Freenove_DHT import DHT 
import RPi.GPIO as GPIO

app = Flask(__name__)

#For LED
LED_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

#for dht11
DHTPin = 17
dht = DHT(DHTPin)
temp = dht.getHumidity()
hum = dht.getTemperature()


#For Motor
Motor1 = 22 # Enable Pin
Motor2 = 27 # Input Pin 1
Motor3 = 17 # Input Pin 2

GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)

data={'temperature': temp,'humidity': hum}



@app.route("/") #This is the route you specify (in our case it is likely just / for now)
def home(): #When the route is called it would run this method
    return render_template('dashboard.html', data=data) #What the method runs

@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    data = request.json
    if data['state'] == 'ON':
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    return jsonify(success=True)

@app.route('/toggle_motor', methods=['POST'])
def toggle_motor():
    data = request.json
    if data['state'] == 'ON':
        GPIO.output(Motor1,GPIO.HIGH) # Sets it on
        # Handles direction
        GPIO.output(Motor2,GPIO.LOW)
        GPIO.output(Motor3,GPIO.HIGH) 
    else:
        GPIO.output(Motor1,GPIO.LOW) # Sets it off
        # Handles direction
        GPIO.output(Motor2,GPIO.LOW)
        GPIO.output(Motor3,GPIO.HIGH)
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) #This part should be at the end at all times as anything under won't be ran