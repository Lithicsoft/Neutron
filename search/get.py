import socket
import requests

local_ip = socket.gethostbyname(socket.gethostname())

def Search_Data(type, keyword, page):
    data = {'type': type, 'keyword': keyword, 'page': page}

    url = f'http://{local_ip}:50100/api/search'
    response = requests.post(url, json=data)
    
    if response:
        return response.json()
    else:
        return None
