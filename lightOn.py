import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
LED=24
GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED, GPIO.HIGH)
sleep(1)
#GPIO.cleanup()