import streamlit as st

from atmt import ATMT_STRT

def Search_Data(conn, keyword):
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM information_fts
                  WHERE information_fts MATCH ?''', (keyword,))

    rows = cursor.fetchall()
    
    if len(rows) == 0:
        st.write("No results found")
        ATMT_STRT(keyword)
    else:
        return rows
