import pandas as pd
import streamlit as st

def Search_Data(conn, keyword):
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM information_fts
                  WHERE information_fts MATCH ?''', (keyword,))

    rows = cursor.fetchall()
    
    if len(rows) == 0:
        st.write("No results found")
    else:
        return rows
