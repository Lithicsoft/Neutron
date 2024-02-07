import streamlit as st
import sqlite3

def Search_Data(conn, keyword):
    cursor = conn.cursor()

    cursor.execute('''SELECT * FROM information
                      WHERE title LIKE ? OR text LIKE ? OR description LIKE ? OR keywords LIKE ? OR shorttext LIKE ?''', 
                      ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%'))

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
