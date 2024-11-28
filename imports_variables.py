from flask import Flask, render_template, request, jsonify
import time
import threading
from Freenove_DHT import DHT 
import smtplib
import imaplib
import email
from datetime import datetime
import RPi.GPIO as GPIO
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import policy
from email.parser import BytesParser
import atexit
# Test Sake
import random

import paho.mqtt.subscribe as subscribe

# For LED
LED_PIN = 19
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

# For DHT11
# We should add a avg system to handle big increases or drops
# We should also stop -999 from being read
DHTPin = 13
dht = DHT(DHTPin)
dht.readDHT11()
hum = 0#dht.getHumidity()
temp = 0#dht.getTemperature()
sumCnt = 0
okCnt = 0
dht_is_running = False
threads_active = True
fan_on = False

# For Email
sender_email = "moars700@gmail.com"
sender_password = "ucgu qkwh ltab zapt" # in App password
recipient_email = "giannouleaschris@gmail.com"
email_sent = False
email_body = ""
hostname="192.168.1.161"

#For Motor
Motor1 = 22  # Enable Pin
Motor2 = 27  # Input Pin 1
Motor3 = 17  # Input Pin 2

GPIO.setup(Motor1, GPIO.OUT)
GPIO.setup(Motor2, GPIO.OUT)
GPIO.setup(Motor3, GPIO.OUT)

#For Light Sensor
light_value = 0

#for rfid 
rfid_uid = ""
user_authenticated = True
user_valid = True
email_user_auth = False
user_changed = False

#user thresholds (values set by default)
user_id = 0
temp_threshold = 24
light_threshold = 400
temp = 0.0
hum = 0.0
light = 0.0 
#setting initial variables high to not change whenever a user is not logged in
# temp_threshold = 24
# light_threshold = 400
