# Py2nacos
A tool that allows an app registers itself with Nacos.

## Fetures
Register the app when it starts. 

Send the heartbeat to nacos every 5 seconds.

## Usages
```python
pip install py2nacos
```
```python
NACOS_SERVER_URL='http://localhost:8848/nacos'
SERVICE_NAME='myapp'
SERVICE_IP=127.0.0.1
PORT=5000
from py2nacos import register_to_nacos
register_to_nacos(NACOS_SERVER_URL, SERVICE_NAME, SERVICE_IP, PORT)
```