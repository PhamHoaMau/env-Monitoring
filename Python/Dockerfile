FROM ubuntu
MAINTAINER JWCLab
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install paho-mqtt python-etcd influxdb
COPY mqtt2influxdb.py /home/python/mqtt2influxdb.py
COPY mqtt_pub.py /home/python/mqtt_pub.py
CMD ["/home/python/mqtt_pub.py"]
ENTRYPOINT ["python3"]

