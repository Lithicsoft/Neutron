import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from library.database import Library_Edit_Data

load_dotenv("./config")
GOOGLE_SAFE_BROWSING_API_KEY = os.getenv('GSB_API_KEY')

allowed_extensions = {"http", "https"}

def is_content_safe(link):
    url = 'https://safebrowsing.googleapis.com/v4/threatMatches:find?key=' + GOOGLE_SAFE_BROWSING_API_KEY
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

def edit_data(conn, table_name, site_id, link, title, text, description, keywords, shorttext):
    added = datetime.now()

    try:
        response = requests.get(link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = "\n".join([p.text for p in soup.find_all('p')])
    except requests.ConnectionError:
        return "Error accessing or parsing the website."

    if not is_content_safe(link):
        return "Unsafe content detected. Not editing the database."

    cursor = conn.cursor()
    Library_Edit_Data(cursor, table_name, link, title, text, description, keywords, shorttext, added, site_id)
    conn.commit()
    cursor.close()
    return "Data edited successfully."
