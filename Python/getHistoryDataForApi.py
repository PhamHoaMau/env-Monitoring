import hashlib
import json
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from flask import Flask
from flask import request
import requests

app = Flask(__name__)


def get_token():
    url_base = "http://identity.jwclab.com:32768/login"
    headers = {'Content-Type': 'application/json'}
    user = "admin_stations"
    password = "11111111"
    data = json.dumps({"id": user, "password": password}, indent=4)
    response = requests.post(url=url_base, data=data, headers=headers)

    if response.status_code == 200:
        access_token = json.loads(response.content.decode('utf-8'))
        return access_token['accessToken']
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


def getHistoryDataForApi(access_token, station_id, start_time, end_time):
    influx_client.switch_database(station_id)
    results = influx_client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from %s where'
                                  ' time >= \'%s\' and time <= \'%s\'' % (station_id, start_time, end_time))
    isvalid = False
    hash_arr = getHashBlockchain(access_token, station_id, start_time, end_time)
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
        return str(data_list).replace("[", "").replace("]", "")
    else:
        return "Invalid when compare hash!"


def getNowDataForApi(station_id):
    influx_client.switch_database(station_id)
    end_time = str(datetime.utcnow()).replace(" ", "T") + "Z"
    result = influx_client.query('select "DEVICE_ID", "time", "TMP", "HUM", "DUST", "PH", "UV" from %s where'
                                 ' time >= \'%s\' - 5s limit 1' % (station_id, end_time))
    now_data = list(result.get_points(measurement=station_id))
    return now_data[0]


@app.route('/nowData/<station_id>')
def now(station_id):
    result = getNowDataForApi(station_id)
    return result


@app.route('/historyData/<station_id>,<start_time>,<end_time>')
def history(station_id, start_time, end_time):
    result = getHistoryDataForApi(token, station_id, start_time, end_time)
    return result


if __name__ == '__main__':
    database_trigger = "trigger_time"
    influx_client = InfluxDBClient(host='178.128.107.247', port=8086)
    token = get_token()
    app.run(host="0.0.0.0", port=5000)
