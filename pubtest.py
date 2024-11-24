import paho.mqtt.subscribe as subscribe

msg = subscribe.simple("IoTlab/EPS32", hostname="192.168.48.140")
print("%s %s" % (msg.topic, msg.payload))

msg2 = subscribe.simple("IoTlab/RFID", hostname="192.168.48.140")
print("%s %s" % (msg2.topic, msg2.payload))