from account.loader import account_database_loader
from account.reliability import get_user_reliability
from app import app
from flask import render_template, request

from manager.call import manager_edit_data, manager_get_id, manager_insert_data, manager_remove_data

conn = account_database_loader()
cursor = conn.cursor()

@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    User = request.cookies.get('USERNAME')
    if User is None:
        User = 'Account'

    return render_template(
        '/contribute/index.html',
        User=User
    )

@app.route('/contribute/insert', methods=['GET', 'POST'])
def contribute_insert():
    if request.form.get('add_button') == 'add_clicked':
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_reliability(cursor, username, password, False)

        if username is None or password is None or login is None:
            message_call = "Unable to verify user, looks like you are not logged in to your account, please log in to take any action on the database."
        else:
            type = request.form.get('type')
            link = request.form.get('link')
            title = request.form.get('title')
            text = request.form.get('text')
            description = request.form.get('description')
            keywords = request.form.get('keywords')
            shorttext = request.form.get('shorttext')
            message_call = manager_insert_data(type, username, password, link, title, text, description, keywords, shorttext)
        
        User = request.cookies.get('USERNAME')
        if User is None:
            User = 'Account'

        return render_template(
            '/contribute/index.html',
            User=User,
            message=message_call
        )

@app.route('/contribute/change', methods=['GET', 'POST'])
def contribute_change():
    if request.form.get('edit_button') == 'edit_clicked':
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_reliability(cursor, username, password, False)

        if username is None or password is None or login is None:
            message_call = "Unable to verify user, looks like you are not logged in to your account, please log in to take any action on the database."
        else:
            site_id = request.form.get('site_id')
            type = request.form.get('type')
            link = request.form.get('link')
            title = request.form.get('title')
            text = request.form.get('text')
            description = request.form.get('description')
            keywords = request.form.get('keywords')
            shorttext = request.form.get('shorttext')
            message_call = manager_edit_data(type, username, password, site_id, link, title, text, description, keywords, shorttext)
        
        User = request.cookies.get('USERNAME')
        if User is None:
            User = 'Account'

        return render_template(
            '/contribute/index.html',
            User=User,
            message=message_call
        )

@app.route('/contribute/remove', methods=['GET', 'POST'])
def contribute_remove():
    if request.form.get('remove_button') == 'remove_clicked':
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_reliability(cursor, username, password, False)

        if username is None or password is None or login is None:
            message_call = "Unable to verify user, looks like you are not logged in to your account, please log in to take any action on the database."
        else:
            site_id = request.form.get('site_id')
            type = request.form.get('type')
            message_call = manager_remove_data(type, username, password, site_id)

        User = request.cookies.get('USERNAME')
        if User is None:
            User = 'Account'

        return render_template(
            '/contribute/index.html',
            User=User,
            message=message_call
        )

@app.route('/contribute/getid', methods=['GET', 'POST'])
def contribute_getid():
    if request.form.get('find_button') == 'find_clicked':
        link = request.form.get('link')
        type = request.form.get('type')
        message_call=manager_get_id(type, link)

        User = request.cookies.get('USERNAME')
        if User is None:
            User = 'Account'

        return render_template(
            '/contribute/index.html',
            User=User,
            message=message_call
        )