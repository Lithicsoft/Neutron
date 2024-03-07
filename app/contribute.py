from account.loader import account_database_loader
from account.reliability import get_user_reliability
from app import app
from flask import render_template, request

from manager.call import manager_edit_data, manager_insert_data, manager_remove_data

conn = account_database_loader()
cursor = conn.cursor()

@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    return render_template(
        'contribute/index.html',
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
            type = request.args.get('type', '')
            link = request.args.get('link', '')
            title = request.args.get('title', '')
            text = request.args.get('text', '')
            description = request.args.get('description', '')
            keywords = request.args.get('keywords', '')
            shorttext = request.args.get('shorttext', '')
            message_call = manager_insert_data(type, username, password, link, title, text, description, keywords, shorttext)
        return render_template(
            'contribute/index.html',
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
            site_id = request.args.get('site_id', '')
            type = request.args.get('type', '')
            link = request.args.get('link', '')
            title = request.args.get('title', '')
            text = request.args.get('text', '')
            description = request.args.get('description', '')
            keywords = request.args.get('keywords', '')
            shorttext = request.args.get('shorttext', '')
            message_call = manager_edit_data(type, username, password, site_id, link, title, text, description, keywords, shorttext)
        return render_template(
            'contribute/index.html',
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
            site_id = request.args.get('site_id', '')
            type = request.args.get('type', '')
            message_call = manager_remove_data(type, username, password, site_id)
        return render_template(
            'contribute/index.html',
            message=message_call
        )
