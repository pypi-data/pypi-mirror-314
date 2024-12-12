from src.py_request_nacos import register_to_nacos

nacos_url='http://82.157.147.8:8848/nacos'
server_name='example'
ip='127.0.0.1'
port=1234
register_to_nacos(nacos_url, server_name, ip, port)