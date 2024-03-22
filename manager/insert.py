import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from library.database import Library_Get_Max_ID, Library_Insert_Data, content_exists

GOOGLE_SAFE_BROWSING_API_KEY = os.environ.get('GSB_API_KEY')

allowed_extensions = {"http", "https"}

def is_content_safe(link):
    url = 'https://safebrowsing.googleapis.com/v4/threatMatches:find?key=' + str(GOOGLE_SAFE_BROWSING_API_KEY)
    payload = {
        "client": {
            "clientId": "your-client-id",
            "clientVersion": "1.5.2"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": link}]
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        data = response.json()
        if 'matches' in data and data['matches']:
            return False
    return True

def insert_data(conn, type, link, title, text, description, keywords, shorttext):
    added = datetime.now()

    cursor = conn.cursor()
    max_site_id = Library_Get_Max_ID(cursor)
    if max_site_id is None:
        site_id = 1
    else:
        site_id = max_site_id + 1

    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = "\n".join([p.text for p in soup.find_all('p')])
    except requests.RequestException as e:
        return "Error accessing or parsing the website."

    if content_exists(conn, type, link):
        return "Content already exists in the database."

    if not is_content_safe(link):
        return "Unsafe content detected. Not inserting into the database."

    cursor = conn.cursor()
    Library_Insert_Data(cursor, type, site_id, link, title, text, description, keywords, shorttext, added)
    conn.commit()
    cursor.close()
    return "Data inserted successfully."
