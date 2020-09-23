import hashlib
import json
import requests
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import os, time


def get_list_db(influx_client):
    db_list = influx_client.get_list_database()
    databases = set()
    for k in range(0, len(db_list)):
        if db_list[k]['name'][-7:] == "station":
            databases.add(db_list[k]['name'])
    return databases


def getTimeBackup(influxdb_client, trigger_db, station_id, time_now):
    datetime_default = "2020-01-01T00:00:00Z"
    databases = influxdb_client.get_list_database()
    isExistDB = False
    for k in range(0, len(databases)):
        if databases[k]['name'] == trigger_db:
            isExistDB = True
            break
    json_body = [
        {
            "measurement": trigger_db,
            "fields": {
                "%s_backup" % station_id: time_now
            }
        }
    ]
    if isExistDB:
        influxdb_client.switch_database(trigger_db)
        result = influxdb_client.query('select "%s_backup" from %s' % (station_id, trigger_db))
        if len(result) == 0:
            influxdb_client.write_points(json_body)
            return datetime_default
        else:
            backup_time = list(result.get_points(measurement=trigger_db))[-1]
            influxdb_client.write_points(json_body)
            return backup_time['%s_backup' % station_id]
    else:
        influxdb_client.create_database(trigger_db)
        influxdb_client.switch_database(trigger_db)
        influxdb_client.write_points(json_body)
        return datetime_default


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


def getHashBlockchain(accesstoken, station_id, start_time, end_time):
    url_base = "http://identity.jwclab.com:32768/historybytime"
    headers = {'Content-Type': 'application/json',
               'x-access-token': accesstoken}
    data = json.dumps({"id": station_id, "start": start_time, "end": end_time}, indent=4)
    response = requests.post(url=url_base, data=data, headers=headers)

    if response.status_code == 200:
        hash_arr = json.loads(response.content.decode('utf-8'))
        return hash_arr
    else:
        return response.status_code


def hashDataInfluxdb(station_id, start_time, end_time):
    influx_client = InfluxDBClient(host='178.128.107.247', port=8086)
    influx_client.switch_database(station_id)

    results = influx_client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from %s where'
                                  ' time >= \'%s\' and time <= \'%s\'' % (station_id, start_time, end_time))
    data_list = list(results.get_points(measurement=station_id))

    md5_hash = hashlib.md5()
    for k in range(0, len(data_list)):
        # print(data_list[k])
        data_encoded = json.dumps(data_list[k]).encode()
        md5_hash.update(data_encoded)
    return md5_hash.hexdigest()


def backupDataToText(influx_client, access_token):
    databases = get_list_db(influx_client)
    for station_id in databases:
        print(station_id)
        influx_client.switch_database(station_id)
        # now = str(datetime.utcnow()).replace(" ", "T") + "Z"
        now = "2020-09-24T00:00:00Z"
        # start_time = getTimeBackup(influx_client, database_trigger, station_id, now)
        # print(type(getTimeBackup(influx_client, database_trigger, station_id, now)))
        start_time = "2020-09-20T01:19:48.767865Z"
        # print('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from %s where'
        #       ' time >= \'%s\' and time <= \'%s\'' % (station_id, start_time, now))
        results = influx_client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from %s where'
                                      ' time >= \'%s\' and time <= \'%s\'' % (station_id, start_time, now))

        isvalid = False
        hash_arr = getHashBlockchain(access_token, station_id, start_time, now)
        for k in range(0, len(hash_arr['response'])):
            time_range = str(hash_arr['response'][k]['range']).split("--")
            start = time_range[0]
            end = datetime.strptime(time_range[1][:-8] + 'Z', '%Y-%m-%dT%H:%M:%SZ') + timedelta(seconds=1)
            blockchain_hash = hash_arr['response'][k]['hash']
            influx_hash = hashDataInfluxdb(station_id, start, end)
            if blockchain_hash != influx_hash:
                isvalid = False
            else:
                isvalid = True

        if isvalid:
            data_list = list(results.get_points(measurement=station_id))
            file_dir = "/tmp/backup/" + station_id + "/"
            try:
                os.mkdir(file_dir)
            except:
                pass
            path = file_dir + now[:10] + ".txt"
            print(path)
            file = open(path, "w")
            for k in range(0, len(data_list)):
                file.write(str(data_list[k]).replace("{", "").replace("}", "").replace("'", "") + "\n")
            file.close()
        else:
            print("Invalid when compare hash!")


if __name__ == '__main__':
    database_trigger = "trigger_time"
    client = InfluxDBClient(host='178.128.107.247', port=8086)
    # while True:
    #     backupDataToText(client)
    #     time.sleep(86400)
    token = get_token()
    print(token)
    backupDataToText(client, token)
