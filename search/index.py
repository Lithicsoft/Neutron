import streamlit as st
import sqlite3

def summary(text):
    words = text.split()
    if len(words) <= 30:
        return text
    else:
        return ' '.join(words[:30]) + ' ...'

def Search_Data(conn, keyword):
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM information
                      WHERE name LIKE ? OR address LIKE ?''', ('%' + keyword + '%', '%' + keyword + '%'))

    rows = cursor.fetchall()
    conn.close()
    
    if len(rows) == 0:
        st.write("No results found")
    else:
        for row in rows:
            st.write(row[0])
            st.write(row[1])
            st.write(summary(row[2]))
            st.markdown("---")
