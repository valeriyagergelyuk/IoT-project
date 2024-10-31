from flask import Flask, render_template, request, jsonify
from datetime import datetime
from Freenove_DHT import DHT 
import RPi.GPIO as GPIO
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import threading  # Import threading
from pprint import pprint
from email import policy
from email.parser import BytesParser

app = Flask(__name__)

# For LED
LED_PIN = 19
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Disable warnings
GPIO.setup(LED_PIN, GPIO.OUT)

# For DHT11
DHTPin = 13
dht = DHT(DHTPin)
dht.readDHT11()
hum = dht.getHumidity()
temp = dht.getTemperature()

# For Motor
Motor1 = 22  # Enable Pin
Motor2 = 27  # Input Pin 1
Motor3 = 17  # Input Pin 2

GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)
GPIO.setup(Motor3, GPIO.OUT)

data = {'temperature': temp, 'humidity': hum}

def send_email():
    sender_email = "moars700@gmail.com"
    sender_password = "ucgu qkwh ltab zapt" # in App password
    recipient_email = "giannouleaschris@gmail.com"

    subject = "Temperature Alert"
    body = "The temperature has exceeded 24 degrees Celsius."

    
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
            time.sleep(2)

            capture_email(date_email_sent)
    except Exception as e:
        print(f"Error sending email: {e}")

def capture_email(date_email_sent):
    mail_received = False
    tries = 4

    sender_email = "moars700@gmail.com"
    sender_password = "ucgu qkwh ltab zapt"
    mail = imaplib.IMAP4_SSL('smtp.gmail.com')

    #logging in
    mail.login(sender_email, sender_password)

    #looping while the email has not been received
    while mail_received == False:
        
        mail.select('inbox')
        status, data = mail.search(None, 'SUBJECT "Temperature Alert"')
        
        #list of emails
        mails = data[0].split()

        #looping through the emails if there are any
        if mails:
            for email_id in mails:
                
                status, info = mail.fetch(email_id, '(RFC822)')
                
                for response_part in info:
                    if isinstance(response_part, tuple):
                        # Parse the email content
                        message = BytesParser(policy=policy.default).parsebytes(response_part[1])
                        
                        mail_from = message['from']
                        date_str = message["Date"]
                        mail_body = None
                        first_line = None

                        # Extracting the body
                        if message.is_multipart():
                            for part in message.iter_parts():
                                if part.get_content_type() == 'text/plain':
                                    mail_body = part.get_payload(decode=True).decode().strip()
                                    first_line = mail_body.splitlines()[0]
                                    break
                                    
                        # Debug information
                        print(mail_from)
                        print(first_line)
                        print(date_str)

                        #checking if the email is valied
                    if first_line == 'Yes': # and mail_date > date_email_sent:
                        mail_received = True
                        print("Fan Turning On")
                            #activate the motor
                    elif first_line == 'No':
                        print("Fan Not Turning On")

        #tries = tries - 1
        #print("Retrying...")                   
        #time.sleep(5)
        #if(tries == 0):
        #    print("Failed to recieve email")
        #    break


def loop():
    global hum, temp
    sumCnt = 0
    okCnt = 0
    email_sent = False  # Flag to track if the email has been sent

    while True:
        sumCnt += 1
        chk = dht.readDHT11()   
        if chk == 0:
            okCnt += 1      
        
        okRate = 100.0 * okCnt / sumCnt
        temperature = 24

        print("sumCnt : %d, \t okRate : %.2f%% "%(sumCnt, okRate))
        print("chk : %d, \t Humidity : %.2f, \t Temperature : %.2f "%(chk, dht.getHumidity(), temperature))

        # Update humidity and temperature for the web server
        hum = dht.getHumidity()
        temp = temperature

        # Check temperature and send email if necessary
        if temperature > 20 and not email_sent:
            send_email()  # Send email
            email_sent = True  # Set flag to indicate email has been sent
        elif temperature <= 20:
            email_sent = False  # Reset the flag if temperature goes below 24

        time.sleep(3)

@app.route("/") 
def home(): 
    return render_template('dashboard.html', data={'temperature': temp, 'humidity': hum}) 

@app.route('/toggle_led', methods=['POST'])
def toggle_led():
    data = request.json
    if data['state'] == 'ON':
        GPIO.output(LED_PIN, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
    return jsonify(success=True)

# @app.route('/toggle_motor', methods=['POST'])
# def toggle_motor():
#     data = request.json
#     if data['state'] == 'ON':
#         GPIO.output(Motor1, GPIO.HIGH)  # Sets it on
#         # Handles direction
#         GPIO.output(Motor2, GPIO.LOW)
#         GPIO.output(Motor3, GPIO.HIGH) 
#     else:
#         GPIO.output(Motor1, GPIO.LOW)  # Sets it off
#         # Handles direction
#         GPIO.output(Motor2, GPIO.LOW)
#         GPIO.output(Motor3, GPIO.HIGH)
#     return jsonify(success=True)

# @app.route('/respond_fan', methods=['POST'])
# def respond_fan():
#     data = request.json
#     if data['response'] == 'yes':
#         GPIO.output(Motor1, GPIO.HIGH)  # Turn on the fan
#         return jsonify(success=True, message="Fan turned on.")
#     else:
#         return jsonify(success=False, message="No action taken.")

if __name__ == "__main__":
    # Start the temperature monitoring loop in a separate thread
    threading.Thread(target=loop, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000) 
