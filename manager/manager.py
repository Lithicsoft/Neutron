from flask import request
from app import app, databases
from .getid import Get_ID
from log.write import db_log, log
from account.authentication import get_user_authentication
from .edit import edit_data
from .insert import insert_data
from .remove import remove_data

conn = databases.conn

account_conn = databases.account_conn
cursor = account_conn.cursor()

def manager_insert_data(type, username, password, link, title, text, description, keywords, shorttext):
    authentication = get_user_authentication(cursor, username, password, False)

    if authentication is None:
        return "Account does not exist."

    if authentication >= 0:
        db_log(log(cursor, username, password, "Insert Data", "Link: " + link + " Title: " + title + " ShortText: " + shorttext))
        insert_data_message = insert_data(conn, type, link, title, text, description, keywords, shorttext)
        return insert_data_message
    else: 
        return "The user's authentication cannot be determined."

def manager_edit_data(type, username, password, site_id, link, title, text, description, keywords, shorttext):
    authentication = get_user_authentication(cursor, username, password, False)

    if authentication is None:
        return "Account does not exist."
    
    if authentication >= 0:
        db_log(log(cursor, username, password, "Edit Data", "Site ID: " + site_id + " Link: " + link + " Title: " + title + " ShortText: " + shorttext))
        edit_data_message = edit_data(conn, type, site_id, link, title, text, description, keywords, shorttext)
        return edit_data_message
    else: 
        return "The user's authentication cannot be determined."

def manager_remove_data(type, username, password, site_id):
    authentication = get_user_authentication(cursor, username, password, False)

    if authentication is None:
        return "Account does not exist."
    
    if authentication >= 0:
        remove_data(conn, type, site_id)
        db_log(log(cursor, username, password, "Remove Data", "Site ID: " + site_id))
        return "Data removed successfully."
    else: 
        return "The user's authentication cannot be determined."

@app.route('/api/manager', methods=['POST'])
def manager():
    data = request.get_json()
    call = data['call']
    type = data['type']
    username = data['username']
    password = data['password']
    site_id = data['site_id']
    link = data['link']
    title = data['title']
    text = data['text']
    description = data['description']
    keywords = data['keywords']
    shorttext = data['shorttext']

    if call == 'insert':
        return_result = manager_insert_data(type, username, password, link, title, text, description, keywords, shorttext)
        return return_result
    elif call == 'edit':
        return_result = manager_edit_data(type, username, password, site_id, link, title, text, description, keywords, shorttext)
        return return_result
    elif call == 'remove':
        return_result = manager_remove_data(type, username, password, site_id)
        return return_result
    elif call == 'getid':
        return_result = Get_ID(conn, type, link)
        return str(return_result)
