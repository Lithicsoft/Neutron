import requests

def Search_Data(type, keyword):
    data = {'type': type, 'keyword': keyword}

    response = requests.post('http://192.168.1.4:5000/search-index', json=data)
    data = response.json()
    
    return response.json()
