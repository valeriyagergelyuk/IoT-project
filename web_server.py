from flask import Flask, render_template, request, jsonify
import time
import threading
import RPi.GPIO as GPIO
import atexit

import paho.mqtt.subscribe as subscribe

app = Flask(__name__)

# For LED
LED_PIN = 19
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

# For PhotoResistor
int photoResistorPin = 4

# For Email
sender_email = "moars700@gmail.com"
sender_password = "ucgu qkwh ltab zapt" # in App password
recipient_email = "giannouleaschris@gmail.com"

def clean_up_before_exit():
    print(" Cleaning...")
    GPIO.cleanup()

def send_email():
    subject = "Light Alert"

    body = "The Light is ON at hh: mm time."

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
            date_email_sent = datetime.now()
            print("Email sent successfully!")
            time.sleep(5)
    except Exception as e:
        print(f"Error sending email: {e}")

def loop():
    while True:
        msg = subscribe.simple("IoTlab/EPS32", hostname="192.168.48.140")
        print("%s %s" % (msg.topic, msg.payload))

        int lightpin = analogRead(photoResistorPin)

        print(lightpin)

        if(lightpin >= 400)
        {
            send_email()
        }

        time.sleep(3)

# Loads the webpage
@app.route("/") 
def home(): 
    return render_template('dashboard.html', data={'temperature': temp, 'humidity': hum}) 

# Toggles the led on the breadboard
@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    data = request.json
    if data['state'] == 'ON':
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    return jsonify(success=True)

# Activates the function to be called when shutdown
atexit.register(clean_up_before_exit)

if __name__ == "__main__":
    # Creates a thread to have it constantly check if it should send a email
    ## Im not sure why there a thread here, it has while True: which should never end?
    ## I think it should just call the function here
    threading.Thread(target=loop, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000) 
