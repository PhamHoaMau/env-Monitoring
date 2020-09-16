#!/usr/bin/env python
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime, json

def on_connect(client, userdata, flags, rc):
    client.subscribe("jwclab/#")

def on_message(client, userdata, msg):
    dict_data = json.loads(msg.payload.decode("utf-8"))
    json_body = [
        {
            "measurement": str(msg.topic).split("/")[1],
            "fields": {
                "DEVICE_ID": dict_data['DEVICE_ID'],
                "TMP": dict_data['TMP'],
                "HUM": dict_data['HUM'],
                "DUST": dict_data['DUST'],
                "UV": dict_data['UV'],
                "PH": dict_data['PH']
            }
        }
    ]
    for database in databases:
        if str(msg.topic).split("/")[1] == database:
            influx_client.switch_database(database)
            influx_client.write_points(json_body)
    # print("Write data from %s to influxdb---> Done!" %(str(msg.topic).split("/")[1]))
    

influx_client = InfluxDBClient('178.128.107.247', 8086)
databases = ['lienchieu_stations', 'haichau_stations', 'camle_stations']
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("178.128.107.247", 1883)

client.loop_forever()