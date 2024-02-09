import streamlit as st
import sqlite3
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from urllib.parse import urlparse
from os.path import splitext

GOOGLE_SAFE_BROWSING_API_KEY = 'API_KEY'

allowed_extensions = {"http", "https"}

def content_exists(conn, link):
    with conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(*) FROM information WHERE link = ?''', (link,))
        count = cursor.fetchone()[0]
        return count > 0

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

def edit_data(conn, site_id, link, title, text, description, keywords, shorttext):
    added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    normalize_link = link

    try:
        response = requests.get(normalize_link)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = "\n".join([p.text for p in soup.find_all('p')])
    except requests.RequestException as e:
        st.error("Error accessing or parsing the website.")
        return

    if not is_content_safe(normalize_link):
        st.warning("Unsafe content detected. Not editing the database.")
        return

    with conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''UPDATE information 
                              SET link=?, title=?, text=?, description=?, keywords=?, shorttext=?, added=?
                              WHERE site_id=?''', 
                           (normalize_link, title, text, description, keywords, shorttext, added, site_id))
            conn.commit()
            st.success("Data edited successfully.")
        except sqlite3.Error as e:
            st.error("Error editing data in the database:", e)

    cursor.close()
