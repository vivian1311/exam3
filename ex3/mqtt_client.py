import paho.mqtt.client as paho
import time
import matplotlib.pyplot as plt
import numpy as np
import serial

# MQTT broker hosted on local machine
mqttc = paho.Client()

host = "localhost"
topic = "Mbed"

# XBee 
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600)

s.write("+++".encode())
char = s.read(2)
print("Enter AT mode.")
print(char.decode())

s.write("ATMY 0x140\r\n".encode())
char = s.read(3)
print("Set MY 0x140.")
print(char.decode())

s.write("ATDL 0x240\r\n".encode())
char = s.read(3)
print("Set DL 0x240.")
print(char.decode())

s.write("ATID 0x1\r\n".encode())
char = s.read(3)
print("Set PAN ID 0x1.")
print(char.decode())

s.write("ATWR\r\n".encode())
char = s.read(3)
print("Write config.")
print(char.decode())

s.write("ATMY\r\n".encode())
char = s.read(4)
print("MY :")
print(char.decode())

s.write("ATDL\r\n".encode())
char = s.read(4)
print("DL : ")
print(char.decode())

s.write("ATCN\r\n".encode())
char = s.read(3)
print("Exit AT mode.")
print(char.decode())

print("start sending RPC")

# signal
#v = np.arange(0,100,1/100)
t = np.arange(0,10,0.1)
v = np.arange(0,100,0.1)
# Callbacks
def on_connect(self, mosq, obj, rc):
      print("Connected rc: " + str(rc))
def on_message(mosq, obj, msg):
      print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n")
      input_data = msg.payload.decode(encoding = 'UTF-8')
      
      for num in range(0, 100):
            v[num] = input_data
            print("%f", v[num])
            
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