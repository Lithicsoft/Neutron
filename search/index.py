import streamlit as st

from atmt import ATMT_STRT
from search.safe import escape_special_characters

def Search_Data(conn, keyword):
    cursor = conn.cursor()

    safe_keyword = escape_special_characters(keyword)

    cursor.execute('''SELECT * FROM information_fts
                  WHERE information_fts MATCH ?''', (safe_keyword,))

    rows = cursor.fetchall()
    
    if len(rows) == 0:
        st.write("No results found")
        #ATMT_STRT(keyword)
    else:
        return rows
