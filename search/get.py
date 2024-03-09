import socket
import requests

local_ip = socket.gethostbyname(socket.gethostname())

def Search_Data(type, keyword):
    data = {'type': type, 'keyword': keyword}

    url = f'http://{local_ip}:8500/'
    response = requests.post(url, json=data)
    
    if response:
        return response.json()
    else:
        return None
