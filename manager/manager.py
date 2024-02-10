import streamlit as st
from log.write import log
from account.loader import account_database_loader
from account.reliability import get_user_reliability
from initializer.loader import censorship_database_loader
from manager.edit import edit_data
from manager.insert import insert_data
from manager.remove import remove_data
from FTS.update import Update_Virtual_Table

def manager_insert_data(conn, username, password, link, title, text, description, keywords, shorttext):
    account_conn = account_database_loader()
    cursor = account_conn.cursor()

    reliability = get_user_reliability(cursor, username, password)

    if reliability == 0: 
        censorship_conn = censorship_database_loader()
        insert_data(censorship_conn, link, title, text, description, keywords, shorttext)
        st.success("Your add request has been sent to the administrator.")
        censorship_conn.close()
    elif reliability >= 1:
        insert_data(conn, link, title, text, description, keywords, shorttext)
    else: 
        st.error("The user's reliability cannot be determined.")
    
    log(cursor, username, password, "Insert Data", "Link: " + link + " Title: " + title + " Text: " + text + " Description: " + description + " Keywords: " + keywords + " ShortText: " + shorttext)
    
    cursor.close()
    account_conn.close()

    Update_Virtual_Table(conn)

def manager_edit_data(conn, username, password, site_id, link, title, text, description, keywords, shorttext):
    account_conn = account_database_loader()
    cursor = account_conn.cursor()

    reliability = get_user_reliability(cursor, username, password)

    if reliability == 0: 
        censorship_conn = censorship_database_loader()
        edit_data(censorship_conn, site_id, link, title, text, description, keywords, shorttext)
        st.success("Your edit request has been sent to the administrator.")
        censorship_conn.close()
    elif reliability >= 2:
        edit_data(conn, site_id, link, title, text, description, keywords, shorttext)
    else: 
        st.error("The user's reliability cannot be determined.")
    
    log(cursor, username, password, "Edit Data", "Site ID: " + site_id + " Link: " + link + " Title: " + title + " Text: " + text + " Description: " + description + " Keywords: " + keywords + " ShortText: " + shorttext)

    cursor.close()
    account_conn.close()

    Update_Virtual_Table(conn)

def manager_remove_data(conn, username, password, site_id):
    account_conn = account_database_loader()
    cursor = account_conn.cursor()

    reliability = get_user_reliability(cursor, username, password)

    if reliability >= 3:
        remove_data(conn, site_id)
        st.success("Data removed successfully.")
    else: 
        st.error("The user's reliability cannot be determined.")

    log(cursor, username, password, "Remove Data", "Site ID: " + site_id)

    account_conn.close()
    cursor.close()

    Update_Virtual_Table(conn)
