#!/usr/bin/env python
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json
import requests


def get_token():
    url_base = "http://identity.jwclab.com:32768/login"
    headers = {'Content-Type': 'application/json'}
    user = "admin_stations"
    password = "11111111"
    data = json.dumps({"id": user, "password": password}, indent=4)
    response = requests.post(url=url_base, data=data, headers=headers)

    if response.status_code == 200:
        token = json.loads(response.content.decode('utf-8'))
        return token['accessToken']
    else:
        return response.status_code


def check_station(token, station):
    url_base = "http://identity.jwclab.com:32768/getrecord"
    headers = {'Content-Type': 'application/json', 'x-access-token': token}
    station = "INFO_" + station
    data = json.dumps({"id": station}, indent=4)
    response = requests.post(url=url_base, data=data, headers=headers)
    return response.status_code


def on_connect(client, userdata, flags, rc):
    client.subscribe("jwclab/#")


def on_message(client, userdata, msg):
    dict_data = json.loads(msg.payload.decode("utf-8"))
    station_id = str(msg.topic).split("/")[1]
    json_body = [
        {
            "measurement": station_id,
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
    if station_id in databases:
        influx_client.switch_database(station_id)
        influx_client.write_points(json_body)
    else:
        if check_station(token, station_id) == 200:
            databases.add(station_id)
            influx_client.create_database(station_id)
            influx_client.switch_database(station_id)
            influx_client.write_points(json_body)


if __name__ == '__main__':
    token = get_token()
    databases = set()
    client = mqtt.Client()
    client.connect("mqtt.jwclab.com", 1883)
    print("Connected to mqtt broker!")
    influx_client = InfluxDBClient('178.128.107.247', 8086)
    print("Connected to Influxdb!")
    print("Processing...")
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
