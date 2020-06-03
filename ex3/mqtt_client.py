import paho.mqtt.client as paho
import time
import matplotlib.pyplot as plt
import numpy as np
import serial

# MQTT broker hosted on local machine
mqttc = paho.Client()

host = "localhost"
topic = "Mbed"

# signal
v = np.arange(0,2,1/100)
t = np.arange(0,10,0.1)
num = 0
# Callbacks
def on_connect(self, mosq, obj, rc):
      print("Connected rc: " + str(rc))
def on_message(mosq, obj, msg):
      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
      input_data = msg.payload.decode(encoding = 'UTF-8')
      data = input_data
      for num in range(1, 10):
          print("%f", input_data)
            
def on_subscribe(mosq, obj, mid, granted_qos):
      print("Subscribed OK")
def on_unsubscribe(mosq, obj, mid, granted_qos):
      print("Unsubscribed OK")

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe

# Connect and subscribe
print("Connecting to " + host + "/" + topic)
mqttc.connect(host, port=1883, keepalive=60)
mqttc.subscribe(topic, 0)

while(1):
    for i in range(0, 100):
        mesg = v[i]
        mqttc.publish(topic, mesg)
        print(mesg)
        time.sleep(1)

# Loop forever, receiving messages
mqttc.loop_forever()