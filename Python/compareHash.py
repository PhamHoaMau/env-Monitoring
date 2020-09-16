#!/usr/bin/env python
import sys
from influxdb import InfluxDBClient
import hashlib
import json
from datetime import datetime, timedelta

client = InfluxDBClient(host='178.128.107.247', port=8086)
databases = client.get_list_database()
measurements = ""
for k in range(1,len(databases)):
    measurements += " " + databases[k]['name']


def md5_hash(measurement, start_time, end_time):
    # print(id, start_time, end_time, hash)
    # print(measurements[int(id) % 100 - 1])
    client.switch_database(measurement)
    start_time = start_time[:-8] + 'Z'
    end_time = datetime.strptime(end_time[:-8] + 'Z', '%Y-%m-%dT%H:%M:%SZ') + timedelta(seconds=1)
    result = client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from %s where'
                          ' time >= \'%s\' and time <= \'%s\'' % (measurement, start_time, end_time))
    data_list = list(result.get_points(measurement=measurement))
    # print(data_list[0])
    # print(data_list[-1])
    # print(end_time)
    # print(len(data_list))

    hash = hashlib.md5()
    for k in range(0, len(data_list)):
        # print(data_list[k])
        data_encoded = json.dumps(data_list[k]).encode()
        hash.update(data_encoded)
    print(hash.hexdigest())


if __name__ == '__main__':
    md5_hash(sys.argv[1], sys.argv[2], sys.argv[3])
