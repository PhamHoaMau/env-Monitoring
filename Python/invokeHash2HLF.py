#!/usr/bin/env python
from influxdb import InfluxDBClient
import hashlib, sys, json
import json
import requests
import time


def get_token():
    api_url_base = "http://identity.jwclab.com:32768/login"
    headers = {'Content-Type': 'application/json'}
    user = "admin_stations"
    password = "11111111"
    data = json.dumps({"id": user, "password": password}, indent=4)
    response = requests.post(url=api_url_base, data=data, headers=headers)

    if response.status_code == 200:
        token = json.loads(response.content.decode('utf-8'))
        return token['accessToken']
    else:
        return response.status_code


def getHashTimeline(device_id):
    client = InfluxDBClient(host='178.128.107.247', port=8086)
    databases = client.get_list_database()
    isExistTriggerDB = False
    for k in range(0, len(databases)):
        if databases[k]['name'] == databaseName:
            isExistTriggerDB = True
            break
    if isExistTriggerDB:
        client.switch_database(databaseName)
        result = client.query('select "%s_hash" from %s' % (device_id, databaseName))
        if len(result) == 0:
            result = dateTime_default
        else:
            trigger_time = list(result.get_points(measurement=databaseName))[-1]
            result = trigger_time["%s_hash" % device_id]
        return result
    else:
        client.create_database(databaseName)
        client.switch_database(databaseName)
        result = dateTime_default
        return result


def hashNoFilter():
    client = InfluxDBClient(host='178.128.107.247', port=8086)
    db_list = client.get_list_database()
    databases = []
    for k in range(0, len(db_list)):
        if db_list[k]['name'][-7:] == "station":
            databases.append(db_list[k]['name'])
    # print(databases)
    hash_arr = []
    for station_id in databases:
        client.switch_database(station_id)
        hash_timeline = getHashTimeline(station_id)
        # print(hash_timeline)
        result = client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from %s where '
                              'time >= \'%s\'' % (station_id, hash_timeline))
        # print(result)
        data_list = list(result.get_points(measurement=station_id))
        # print(data_list)
        start_time = data_list[0]['time']
        end_time = data_list[-1]['time']
        dateTime = str(start_time) + str("--") + str(end_time)
        station_id = data_list[0]['DEVICE_ID']


        json_body = [
            {
                "measurement": databaseName,
                "fields": {
                    "%s_hash" % station_id: end_time
                }
            }
        ]
        # print(json_body)
        client.switch_database(databaseName)
        client.write_points(json_body)

        md5_hash = hashlib.md5()
        for k in range(0, len(data_list)):
            # print(data_list[k])
            data_encoded = json.dumps(data_list[k]).encode()
            md5_hash.update(data_encoded)
        hash = {'id': station_id, 'dateTime': start_time, 'range': dateTime, 'hash': md5_hash.hexdigest()}
        # print(hash)
        hash_arr.append(hash)
    return hash_arr


def invokeHash():
    url = "http://identity.jwclab.com:32768/add"
    token = get_token()
    headers = {'Content-Type': 'application/json', 'x-access-token': token}
    # print(headers)
    hash_arr = hashNoFilter()

    for data in hash_arr:
        data = json.dumps(data, indent=4)
        response = requests.post(url=url, data=data, headers=headers)
        if response.status_code != 200:
            print(response.status_code)


if __name__ == '__main__':
    datetime_default = "2020-09-23T09:30:00Z"
    databaseName = "trigger_time"
    print("Invoking hash to Hyperledger Fabric...")
    while True:
        invokeHash()
        time.sleep(60)
