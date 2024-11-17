from flask import Flask, render_template, request, jsonify
import time
import threading
import RPi.GPIO as GPIO
import atexit
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import policy
from email.parser import BytesParser
import smtplib
import imaplib
from datetime import datetime

import paho.mqtt.subscribe as subscribe

app = Flask(__name__)

hum = 30
temp = 20

# For LED
LED_PIN = 19
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

# For Email
sender_email = "moars700@gmail.com"
sender_password = "ucgu qkwh ltab zapt" # in App password
recipient_email = "giannouleaschris@gmail.com"

email_sent = False
email_body = ""
light_value = 0

def clean_up_before_exit():
    print(" Cleaning...")
    GPIO.cleanup()

def send_email():
    global email_body
    current_time = datetime.now()
    formatted_time = current_time.strftime("%H:%M")

    subject = "Light Alert"
    email_body = f"The light was turned on at {formatted_time}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls() 
            server.login(sender_email, sender_password)  
            server.send_message(msg) 
            date_email_sessnt = datetime.now()
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def loop():
    global email_sent
    global light_value
    while True:
        # msg = subscribe.simple("IoTlab/EPS32", hostname="192.168.167.140")
        msg = subscribe.simple("IoTlab/EPS32", hostname="192.168.1.18")
        print("%s %s" % (msg.topic, msg.payload))


        light_value = int(msg.payload.decode('utf-8'))

        if(light_value <= 400 and not email_sent):
           send_email()
           email_sent = True
        elif(light_value > 400):
            email_sent = False
        time.sleep(1)

# Loads the webpage
@app.route("/") 
def home(): 
    return render_template('dashboard.html', data={'temperature': temp, 'humidity': hum}) 

@app.route('/get_email_and_light_data')
def returnCurrentDataValues():
    global email_sent
    global light_value
    global email_body
    data = {'Light Amount': light_value, "isEmailSent": email_sent, "emailBody": email_body}
    return jsonify(data)

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
