import paho.mqtt.subscribe as subscribe

msg = subscribe.simple("IoTlab/EPS32", hostname="192.168.0.166")
print("%s %s" % (msg.topic, msg.payload))