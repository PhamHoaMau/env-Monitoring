#!/usr/bin/env python
from influxdb import InfluxDBClient
import sys

def getId(database):
    client = InfluxDBClient(host='178.128.107.247', port=8086)
    client.switch_database(database)
    result = client.query('select "DEVICE_ID" from %s limit 1' %database)
    data_list = list(result.get_points(measurement=database))[0]
    print(data_list['DEVICE_ID'])

if __name__ == '__main__':
    getId(sys.argv[1])