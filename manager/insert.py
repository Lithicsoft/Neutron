import streamlit as st
import sqlite3
import requests
from bs4 import BeautifulSoup
import json

GOOGLE_SAFE_BROWSING_API_KEY = 'API_KEY'

def content_exists(text_content, address):
    with sqlite3.connect('./database/search-index.db') as conn:
        cursor = conn.cursor()
        if text_content:
            cursor.execute('''SELECT COUNT(*) FROM information WHERE text = ?''', (text_content,))
        else:
            cursor.execute('''SELECT COUNT(*) FROM information WHERE address = ?''', (address,))
        count = cursor.fetchone()[0]
        return count > 0

def is_content_safe(text_content):
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
            "threatEntries": [{"url": text_content}]
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

def insert_data(name, address):
    try:
        response = requests.get(address)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = "\n".join([p.text for p in soup.find_all('p')])
    except requests.RequestException as e:
        st.error("Error accessing or parsing the website:", e)
        return

    if content_exists(text_content, address):
        st.warning("Content already exists in the database.")
        return

    if not is_content_safe(address):
        st.warning("Unsafe content detected. Not inserting into the database.")
        return

    with sqlite3.connect('./database/search-index.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO information (name, address, text)
                            VALUES (?, ?, ?)''', (name, address, text_content))
            conn.commit()
            st.success("Data inserted successfully.")
        except sqlite3.Error as e:
            st.error("Error inserting data into the database:", e)
