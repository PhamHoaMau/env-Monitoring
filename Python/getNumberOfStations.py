#!/usr/bin/env python
from influxdb import InfluxDBClient

client = InfluxDBClient(host='178.128.107.247', port=8086)
databases = client.get_list_database()
results = ""
for k in range(1,len(databases)):
    results += " " + databases[k]['name']
print(results)



