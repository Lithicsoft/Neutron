from flask import Flask, request
import sys
import os
sys.path.append(os.path.abspath(os.path.join('./')))
from initializer.loader import database_loader
from log.write import log
from account.loader import account_database_loader
from account.reliability import get_user_reliability
from initializer.loader import censorship_database_loader, database_loader
from edit import edit_data
from insert import insert_data
from remove import remove_data
from FTS.update import Update_Virtual_Table

conn0 = database_loader(0)
conn1 = database_loader(1)
conn2 = database_loader(2)
censorship_conn0 = censorship_database_loader(0)
censorship_conn1 = censorship_database_loader(1)
censorship_conn2 = censorship_database_loader(2)

account_conn = account_database_loader()
cursor = account_conn.cursor()

def manager_insert_data(type, username, password, link, title, text, description, keywords, shorttext):
    if type == 'Text':
        conn = conn0
        censorship_conn = censorship_conn0
    elif type == 'Image':
        conn = conn1
        censorship_conn = censorship_conn1
    elif type == 'Video':
        conn == conn2
        censorship_conn - censorship_conn2

    reliability = get_user_reliability(cursor, username, password)

    if reliability == 0: 
        insert_data(censorship_conn, link, title, text, description, keywords, shorttext)
        return "Your add request has been sent to the administrator."
    elif reliability >= 1:
        log(cursor, username, password, "Insert Data", "Link: " + link + " Title: " + title + " Text: " + text + " Description: " + description + " Keywords: " + keywords + " ShortText: " + shorttext)
        Update_Virtual_Table(conn)
        return insert_data(conn, link, title, text, description, keywords, shorttext)
    else: 
        return "The user's reliability cannot be determined."

def manager_edit_data(type, username, password, site_id, link, title, text, description, keywords, shorttext):
    if type == 'Text':
        conn = conn0
        censorship_conn = censorship_conn0
    elif type == 'Image':
        conn = conn1
        censorship_conn = censorship_conn1
    elif type == 'Video':
        conn == conn2
        censorship_conn = censorship_conn2

    reliability = get_user_reliability(cursor, username, password)

    if reliability == 0: 
        edit_data(censorship_conn, site_id, link, title, text, description, keywords, shorttext)
        return "Your edit request has been sent to the administrator."
    elif reliability >= 2:
        log(cursor, username, password, "Edit Data", "Site ID: " + site_id + " Link: " + link + " Title: " + title + " Text: " + text + " Description: " + description + " Keywords: " + keywords + " ShortText: " + shorttext)
        Update_Virtual_Table(conn)
        return edit_data(conn, site_id, link, title, text, description, keywords, shorttext)
    else: 
        return "The user's reliability cannot be determined."

def manager_remove_data(type, username, password, site_id):
    if type == 'Text':
        conn = conn0
    elif type == 'Image':
        conn = conn1
    elif type == 'Video':
        conn == conn2

    reliability = get_user_reliability(cursor, username, password)

    if reliability >= 3:
        remove_data(conn, site_id)
        log(cursor, username, password, "Remove Data", "Site ID: " + site_id)
        Update_Virtual_Table(conn)
        return "Data removed successfully."
    else: 
        return "The user's reliability cannot be determined."

app = Flask(__name__)

@app.route('/', methods=['POST'])
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
        print(return_result)
        return return_result
    elif call == 'edit':
        return_result = manager_edit_data(type, username, password, site_id, link, title, text, description, keywords, shorttext)
        return return_result
    elif call == 'remove':
        return_result = manager_remove_data(type, username, password, site_id)
        return return_result
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501)
