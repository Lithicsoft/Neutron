import streamlit as st
import sqlite3

def Search_Data(conn, keyword):
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM information_fts
                  WHERE information_fts MATCH ?''', (keyword,))

    rows = cursor.fetchall()
    conn.close()
    
    if len(rows) == 0:
        st.write("No results found")
    else:
        for row in rows:
            st.write(row[0]) 
            st.write(row[1])
            st.write(row[2])
            st.write(row[6])
            st.markdown("---")
