#!/usr/bin/env python
import json, time, datetime
from influxdb import InfluxDBClient

data_bef = {'PH': 0, 'DUST': 0, 'TMP': 0, 'UV': 0, 'HUM': 0}


# threshold = {'tmp': 0.005, 'dust': 0.001, 'hum': 0.05, 'uv': 0.01, 'ph': 0.002}
threshold = {'tmp': 0.05, 'dust': 0.01, 'hum': 0.5, 'uv': 0.1, 'ph': 0.02}

client = InfluxDBClient(host='178.128.107.247', port=8086)
client.switch_database("sensors_data")
results = client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from mqtt_consumer '
                       'where time > (now() - 10s) limit 1')
data_list = list(results.get_points(measurement='mqtt_consumer'))
# print(len(data_list))

client.switch_database("iot_data_filtered")

data_points = []

for k in range(0, len(data_list)):
    data_dict = data_list[k]
    if abs(data_dict['TMP'] - data_bef['TMP']) >= threshold['tmp'] * data_bef['TMP'] \
            or abs(data_dict['HUM'] - data_bef['HUM']) >= threshold['hum'] * data_bef['HUM'] \
            or abs(data_dict['DUST'] - data_bef['DUST']) >= threshold['dust'] * data_bef['DUST'] \
            or abs(data_dict['UV'] - data_bef['UV']) >= threshold['uv'] * data_bef['UV'] \
            or abs(data_dict['PH'] - data_bef['PH']) >= threshold['ph'] * data_bef['PH']:
        # print("{}, {}, {}, {}, {}, {}, {}".format(str(data_dict['time'])[0:19], int(data_dict['DEVICE_ID']),
        #     int(data_dict['TMP']), int(data_dict['HUM']), int(data_dict['DUST']),int(data_dict['UV']),
        #     int(data_dict['PH'])))

        data_bef = data_dict
        data_json = {
            "measurement": "iot_data",
            "time": str(data_dict['time'])[0:19],
            "tags": {
                "user": "jwclab"
            },
            "fields": {
                "DEVICE_ID": str(data_dict['DEVICE_ID']),
                "TMP": int(data_dict['TMP']),
                "HUM": int(data_dict['HUM']),
                "DUST": int(data_dict['DUST']),
                "UV": int(data_dict['UV']),
                "PH": int(data_dict['PH'])
            }
        }
        data_points.append(data_json)
if len(data_points) > 0:
    client.write_points(data_points)
    print("Write data at {} ---> {}".format(data_list[0]['time'][:19], "Done!"))
# results = client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from iot_data '
#                       'where time > (now() - 1m) limit 12')
# data_list = list(results.get_points(measurement='iot_data'))
# for data in data_list:
#     print(data)

