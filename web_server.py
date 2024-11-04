from flask import Flask, render_template, request, jsonify
import time
import threading
import RPi.GPIO as GPIO
import smtplib
import imaplib
import email
from datetime import datetime
from Freenove_DHT import DHT 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import policy
from email.parser import BytesParser
import atexit

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
sumCnt = 0
okCnt = 0
dht_is_running = True

# For Email
sender_email = "moars700@gmail.com"
sender_password = "ucgu qkwh ltab zapt" # in App password
recipient_email = "giannouleaschris@gmail.com"

# For Motor
Motor1 = 22  # Enable Pin
Motor2 = 27  # Input Pin 1
Motor3 = 17  # Input Pin 2

GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)
GPIO.setup(Motor3, GPIO.OUT)

fan_on = False

def clean_up_before_exit():
    print(" Cleaning...")
    GPIO.cleanup()

def send_email():
    subject = "Temperature Alert"
    body = "The temperature has exceeded 24 degrees Celsius. Would You like to turn on the fan? Reply with Yes to turn on the fan."

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
            capture_email(date_email_sent)
    except Exception as e:
        print(f"Error sending email: {e}")

def capture_email(date_email_sent):
    yes_mail_received = False
    global fan_on
    global dht_is_running

    # Allows the probing to work while waiting for email
    dht_thread = threading.Thread(target=dht_loop, daemon=True)
    dht_thread.start()

    mail = imaplib.IMAP4_SSL('smtp.gmail.com')
    mail.login(sender_email, sender_password)

    #looping while the email has not been received
    while yes_mail_received == False:
        
        mail.select('inbox')
        status, data = mail.search(None, 'SUBJECT "Temperature Alert"')
        
        #list of emails
        mails = data[0].split()

        #looping through the emails if there are any
        if mails:
            for email_id in reversed(mails):
                
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
                                    # Makng sure to only get one line
                                    first_line = mail_body.splitlines()[0]
                                    break
                                    
                        print(mail_from)
                        print(first_line)
                        print(date_str)

                    if first_line == 'Yes':
                        yes_mail_received = True
                        print("Fan Turning On")
                        fan_on = True
                        # Activates the motor
                        toggle_motor(first_line)
                        # this will get rid of the emai after it has seen it
                        mail.store(email_id, '+FLAGS', '\\Deleted')
                        mail.expunge()

                    elif first_line != None:
                        yes_mail_received = False
                        print("Fan Not Turning On")
                        mail.store(email_id, '+FLAGS', '\\Deleted')
                        mail.expunge()

                if(yes_mail_received == True):
                    # Stops the thread
                    dht_is_running = False
                    break
        
        ## Now the email will wait for a yes always, but if user says no, it won't resend if it dropps down to below 24,
        ## then comes back up uptill the user says yes, should that be changed?

        ## not sure if we should have a limiter of some kind incase the user never replies or the email just fails to send
        ## Rn if something happens to the email where it just never gets sent, it will wait infinty for the response (Atleast i think it would)
        ## Maybe there shuold be something to just resend it after it checks for a response 5 times

def dht_loop():
    global hum, temp, sumCnt, okCnt

    while dht_is_running:
        sumCnt += 1
        chk = dht.readDHT11()   
        if chk == 0:
            okCnt += 1      
        
        okRate = 100.0 * okCnt / sumCnt
        temperature = 25 #dht.getTemperature()
        humditiy = dht.getHumidity()

        print("sumCnt : %d, \t okRate : %.2f%% "%(sumCnt, okRate))
        print("chk : %d, \t Humidity : %.2f, \t Temperature : %.2f "%(chk, humditiy, temperature))

        # Update humidity and temperature for the web server
        hum = humditiy
        temp = temperature
        time.sleep(3)

def toggle_motor(emailResult):
    global fan_on
    if emailResult == 'Yes':
        GPIO.output(Motor1, GPIO.HIGH)  # Sets it on
        # Handles direction
        GPIO.output(Motor2, GPIO.LOW)
        GPIO.output(Motor3, GPIO.HIGH) 
    else:
        fan_on = False
        GPIO.output(Motor1, GPIO.LOW)  # Sets it off

def loop():
    global hum, temp, sumCnt, okCnt
    email_sent = False  # Flag to track if the email has been sent

    while True:
        sumCnt += 1
        chk = dht.readDHT11()   
        if chk == 0:
            okCnt += 1      
        
        okRate = 100.0 * okCnt / sumCnt
        temperature = 25 #dht.getTemperature()
        humditiy = dht.getHumidity()

        print("sumCnt : %d, \t okRate : %.2f%% "%(sumCnt, okRate))
        print("chk : %d, \t Humidity : %.2f, \t Temperature : %.2f "%(chk,humditiy, temperature))

        # Update humidity and temperature for the web server
        hum = humditiy
        temp = temperature

        # Check temperature and send email if necessary
        if temperature > 24 and not email_sent:
            send_email() 
            email_sent = True  # Set flag to indicate email has been sent
        elif temperature <= 24:
            email_sent = False  # Reset the flag if temperature goes below 24
            # This should automatically turn off the motor 
            toggle_motor('off')
        time.sleep(3)

# Loads the webpage
@app.route("/") 
def home(): 
    return render_template('dashboard.html', data={'temperature': temp, 'humidity': hum}) 

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
@app.route('/get_data')
def returnCurrentDataValues():
    global fan_on
    global hum
    global temp
    data = {'IsFanMeantToBeOn': fan_on, "Temperature": temp, "Humidity": hum}
    return jsonify(data)

# Activates the function to be called when shutdown
atexit.register(clean_up_before_exit)

if __name__ == "__main__":
    # Creates a thread to have it constantly check if it should send a email
    ## Im not sure why there a thread here, it has while True: which should never end?
    ## I think it should just call the function here
    threading.Thread(target=loop, daemon=True).start()
    
    app.run(host='0.0.0.0', port=5000) 
