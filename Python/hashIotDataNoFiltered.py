#!/usr/bin/env python
from influxdb import InfluxDBClient
import hashlib, time
import json

client = InfluxDBClient(host='178.128.107.247', port=8086)
databases = client.get_list_database()
measurements = []
for k in range(1,len(databases)):
    measurements.append(databases[k]['name'])

for measurement in measurements:
    client.switch_database(measurement)
    result = client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from %s where '
                          'time >= now() - 10m' % measurement)
    data_list = list(result.get_points(measurement=measurement))
    start = data_list[0]['time']
    end = data_list[-1]['time']
    dateTime = str(start) + str("--") + str(end)
    id = data_list[0]['DEVICE_ID']
    # print(len(data_list))

    hash = hashlib.md5()
    for k in range(0, len(data_list)):
        # print(data_list[k])
        data_encoded = json.dumps(data_list[k]).encode()
        hash.update(data_encoded)
    print("{\"id\":\"%s\",\"dateTime\":\"%s\",\"data\":{\"%s\":\"%s\"}}" %(id, start, dateTime, hash.hexdigest()), end=' ')
