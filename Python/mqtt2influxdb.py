#!/usr/bin/env python
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import datetime, json


def on_connect(client, userdata, flags, rc):
    client.subscribe("jwclab/#")


def on_message(client, userdata, msg):
    dict_data = json.loads(msg.payload.decode("utf-8"))
    print(dict_data)
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
    print(json_body)
    for database in databases:
        if str(msg.topic).split("/")[1] == database:
            influx_client.switch_database(database)
            influx_client.write_points(json_body)


influx_client = InfluxDBClient('178.128.107.247', 8086)
# databases = ['lienchieu_stations', 'haichau_stations', 'camle_stations']
db = influx_client.get_list_database()
databases = []
for k in range(1, len(db)):
    databases.append(db[k]['name'])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.jwclab.com", 1883)
client.loop_forever()
