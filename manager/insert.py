import streamlit as st

import sqlite3
import requests
from bs4 import BeautifulSoup

def insert_data(name, address):
    try:
        response = requests.get(address)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = "\n".join([p.text for p in soup.find_all('p')])
    except requests.RequestException as e:
        st.text("Error accessing or parsing the website:", e)
        return

    with sqlite3.connect('./database/search-index.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO information (name, address, text)
                            VALUES (?, ?, ?)''', (name, address, text_content))
            conn.commit()
        except sqlite3.Error as e:
            st.text("Error inserting data into the database:", e)
