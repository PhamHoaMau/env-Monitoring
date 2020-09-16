#!/usr/bin/env python
from influxdb import InfluxDBClient
import hashlib, time
import json

client = InfluxDBClient(host='178.128.107.247', port=8086, database='sensors_data')
client.switch_database("iot_data_filtered")

# while True:
result = client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from iot_data where time '
                      '>= now() - 15s limit 2')
data_list = list(result.get_points(measurement='iot_data'))
start = data_list[0]['time'][:19]
end = data_list[-1]['time'][:19]
dateTime = str(start) + str("--") + str(end)
id = data_list[0]['DEVICE_ID']
hash = hashlib.md5()
for k in range(0,len(data_list)):
    # print(data_list[k])
    data_encoded = json.dumps(data_list[k]).encode()
    hash.update(data_encoded)
print("{\"id\":\"%s\",\"dataTime\":\"%s\",\"data\":{\"%s\":\"%s\"}}" %(id[:-2], start, dateTime, hash.hexdigest()))