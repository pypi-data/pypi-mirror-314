import requests
import json
import numpy as np

register_service_suffix='/v1/ns/instance'
heartbeat_suffix='/v1/ns/instance/beat'
request_service_suffix='/v1/ns/instance/list'


def request_from_nacos(nacos_url, service_name):
    result = requests.get(nacos_url + request_service_suffix, params={'serviceName': service_name}).text
    result_json = json.loads(result)
    hosts = result_json['hosts']
    host = hosts[np.random.randint(0, len(hosts))]
    return 'http://'+host['ip']+':'+str(host['port'])


import time
import threading
def register_to_nacos(nacos_url, service_name, ip, port):
    result = requests.post(nacos_url + register_service_suffix,
                           data={'serviceName': service_name, 'ip': ip, 'port': port}).text
    threading.Thread(target=heartbeat_to_nacos, args=(nacos_url, service_name, ip, port)).start()
    return result


def heartbeat_to_nacos(nacos_url, service_name, ip, port):
    while True:
        requests.put(nacos_url + heartbeat_suffix, data={'serviceName': service_name, 'ip': ip, 'port': port}).text
        time.sleep(5)
