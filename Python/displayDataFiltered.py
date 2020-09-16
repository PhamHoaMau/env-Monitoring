#!/usr/bin/env python
import json, time, datetime
from influxdb import InfluxDBClient

while True:
    client = InfluxDBClient(host='178.128.107.247', port=8086)
    # client.switch_database("iot_data_filtered")
    # results = client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from iot_data '
    #                       'where time > (now() - 1d) limit 720')
    # data_list = list(results.get_points(measurement='iot_data'))
    # print("{} {}   {}".format("iot_data_filtered ", len(data_list), data_list[-1]['time'][:19]))

    client.switch_database("lienchieu_stations")
    # results = client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from lc_stations')
    #                        # 'where time > (now() - 1h10s) limit 720')
    results = client.query('select * from lienchieu_stations where time > now() - 60s')
    data_list = list(results.get_points(measurement='lienchieu_stations'))
    print("location: {}, data: {}".format("lienchieu_stations", data_list[-1]))

    client.switch_database("haichau_stations")
    # results = client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from lc_stations')
    #                        # 'where time > (now() - 1h10s) limit 720')
    results = client.query('select * from haichau_stations where time > now() - 60s')
    data_list = list(results.get_points(measurement='haichau_stations'))
    print("location: {}, data: {}".format("haichau_stations",data_list[-1]))

    client.switch_database("camle_stations")
    # results = client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from lc_stations')
    #                        # 'where time > (now() - 1h10s) limit 720')
    results = client.query('select * from camle_stations where time > now() - 60s')
    data_list = list(results.get_points(measurement='camle_stations'))
    print("location: {}, data: {}".format("camle_stations",data_list[-1]))
    time.sleep(5)