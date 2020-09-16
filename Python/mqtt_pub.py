#!/usr/bin/env python
from random import randrange
import paho.mqtt.client as mqtt
import time
import json

broker = "178.128.107.247"
port = 1883

client1 = mqtt.Client("")
client1.connect(broker, port)

while True:
    data = {'DEVICE_ID': int(101)}
    data['TMP'] = randrange(40, 45)
    data['HUM'] = randrange(20, 25)
    data['DUST'] = randrange(6, 10)
    data['UV'] = randrange(3, 5)
    data['PH'] = randrange(5, 10)
    lienchieu_stations = json.dumps(data)
    print(lienchieu_stations)
    client1.publish("jwclab/lienchieu_stations", lienchieu_stations)

    data = {'DEVICE_ID': int(102)}
    data['TMP'] = randrange(40, 45)
    data['HUM'] = randrange(20, 25)
    data['DUST'] = randrange(6, 10)
    data['UV'] = randrange(3, 5)
    data['PH'] = randrange(5, 10)
    haichau_stations = json.dumps(data)
    print(haichau_stations)
    client1.publish("jwclab/haichau_stations", haichau_stations)

    data = {'DEVICE_ID': int(103)}
    data['TMP'] = randrange(40, 45)
    data['HUM'] = randrange(20, 25)
    data['DUST'] = randrange(6, 10)
    data['UV'] = randrange(3, 5)
    data['PH'] = randrange(5, 10)
    camle_stations = json.dumps(data)
    print(camle_stations)
    client1.publish("jwclab/camle_stations", camle_stations)
    time.sleep(5)