import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from flask import Flask, render_template
import threading

# MQTT Settings
mqtt_broker = "192.168.1.161"  # IP of the Raspberry Pi MQTT broker
mqtt_port = 1883
mqtt_topic = "light/intensity"

# LED Pin Setup (GPIO)
led_pin = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)


smtp_server = "smtp.gmail.com"
smtp_port = 587
sender_email = "sheldongreen2002@@gmail.com"
receiver_email = "sheldongreen2002@example.com"
email_password = "bwwu onxq wfxu pumi"

app = Flask(__name__)

light_intensity = None
led_status = "OFF"
email_status = None


def on_message(client, userdata, message):
    global light_intensity, led_status, email_status
    
    light_intensity = int(message.payload.decode())
    print(f"Light Intensity: {light_intensity}")

    if light_intensity < 400:
        GPIO.output(led_pin, GPIO.HIGH)
        led_status = "ON"
        email_status = send_email_notification() 
    else:
        GPIO.output(led_pin, GPIO.LOW)  
        led_status = "OFF"
        email_status = None


def send_email_notification():
    current_time = datetime.now().strftime("%H:%M")
    subject = "The Light is ON"
    body = f"The Light is ON at {current_time}."
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, email_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
        return "Email has been sent"
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html', light_intensity=light_intensity, led_status=led_status, email_status=email_status)

# Set up MQTT client
client = mqtt.Client()
client.on_message = on_message


client.connect(mqtt_broker, mqtt_port, 60)
client.subscribe(mqtt_topic)

# Start the MQTT loop in a separate thread
def start_mqtt_loop():
    client.loop_forever()

if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=start_mqtt_loop)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    
    app.run(host='0.0.0.0', port=5000)
