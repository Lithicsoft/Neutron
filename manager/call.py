import requests

def manager_insert_data(type, username, password, link, title, text, description, keywords, shorttext):
    site_id = None
    data = {'call': 'insert', 'type': type, 'username': username, 'password': password, 'site_id': site_id, 'link': link, 'title': title, 'text': text, 'description': description, 'keywords': keywords, 'shorttext': shorttext}

    response = requests.post('http://192.168.1.4:8501/manager', json=data)

    return response.text

def manager_edit_data(type, username, password, site_id, link, title, text, description, keywords, shorttext):
    data = {'call': 'edit', 'type': type, 'username': username, 'password': password, 'site_id': site_id, 'link': link, 'title': title, 'text': text, 'description': description, 'keywords': keywords, 'shorttext': shorttext}

    response = requests.post('http://192.168.1.4:8501/manager', json=data)
    
    return response.text

def manager_remove_data(type, username, password, site_id):
    link = None
    title = None
    text = None
    description = None
    keywords = None
    shorttext = None
    data = {'call': 'remove', 'type': type, 'username': username, 'password': password, 'site_id': site_id, 'link': link, 'title': title, 'text': text, 'description': description, 'keywords': keywords, 'shorttext': shorttext}

    response = requests.post('http://192.168.1.4:8501/manager', json=data)
    
    return response.text
