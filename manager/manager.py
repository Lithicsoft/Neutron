import streamlit as st
from account.loader import account_database_loader
from account.reliability import get_user_reliability
from initializer.loader import censorship_database_loader
from manager.edit import edit_data
from manager.insert import insert_data
from manager.remove import remove_data

def manager_insert_data(conn, username, password, link, title, text, description, keywords, shorttext):
    account_conn = account_database_loader()
    cursor = account_conn.cursor()

    reliability = get_user_reliability(cursor, username, password)

    if reliability == 0: 
        censorship_conn = censorship_database_loader()
        insert_data(censorship_conn, link, title, text, description, keywords, shorttext)
        st.success("Your add request has been sent to the administrator.")
        censorship_conn.close()
    elif reliability == 1:
        insert_data(conn, link, title, text, description, keywords, shorttext)
    else: 
        st.error("The user's reliability cannot be determined.")
    
    cursor.close()
    account_conn.close()

def manager_edit_data(conn, username, password, site_id, link, title, text, description, keywords, shorttext):
    account_conn = account_database_loader()
    cursor = account_conn.cursor()

    reliability = get_user_reliability(cursor, username, password)

    if reliability == 0: 
        censorship_conn = censorship_database_loader()
        edit_data(censorship_conn, site_id, link, title, text, description, keywords, shorttext)
        st.success("Your edit request has been sent to the administrator.")
        censorship_conn.close()
    elif reliability == 1:
        edit_data(conn, site_id, link, title, text, description, keywords, shorttext)
    else: 
        st.error("The user's reliability cannot be determined.")
    
    cursor.close()
    account_conn.close()

def manager_remove_data(conn, username, password, site_id):
    account_conn = account_database_loader()
    cursor = account_conn.cursor()

    reliability = get_user_reliability(cursor, username, password)

    if reliability == 1:
        remove_data(conn, site_id)
        st.success("Data removed successfully.")
    account_conn.close()
    cursor.close()


