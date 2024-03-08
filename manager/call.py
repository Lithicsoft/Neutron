import socket
import requests

local_ip = socket.gethostbyname(socket.gethostname())

def manager_insert_data(type, username, password, link, title, text, description, keywords, shorttext):
    site_id = None
    data = {'call': 'insert', 'type': type, 'username': username, 'password': password, 'site_id': site_id, 'link': link, 'title': title, 'text': text, 'description': description, 'keywords': keywords, 'shorttext': shorttext}

    response = requests.post(f'http://{local_ip}:8501/', json=data)

    return response.text

def manager_edit_data(type, username, password, site_id, link, title, text, description, keywords, shorttext):
    data = {'call': 'edit', 'type': type, 'username': username, 'password': password, 'site_id': site_id, 'link': link, 'title': title, 'text': text, 'description': description, 'keywords': keywords, 'shorttext': shorttext}

    response = requests.post(f'http://{local_ip}:8501/', json=data)
    
    return response.text

def manager_remove_data(type, username, password, site_id):
    link = None
    title = None
    text = None
    description = None
    keywords = None
    shorttext = None
    data = {'call': 'remove', 'type': type, 'username': username, 'password': password, 'site_id': site_id, 'link': link, 'title': title, 'text': text, 'description': description, 'keywords': keywords, 'shorttext': shorttext}

    response = requests.post(f'http://{local_ip}:8501/', json=data)
    
    return response.text

def manager_get_id(type, link):
    site_id = None
    username = None
    password = None
    title = None
    text = None
    description = None
    keywords = None
    shorttext = None
    data = {'call': 'getid', 'type': type, 'username': username, 'password': password, 'site_id': site_id, 'link': link, 'title': title, 'text': text, 'description': description, 'keywords': keywords, 'shorttext': shorttext}

    response = requests.post(f'http://{local_ip}:8501/', json=data)

    return response.text