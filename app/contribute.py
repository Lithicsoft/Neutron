from account.loader import account_database_loader
from account.authentication import get_user_authentication
from app import app
from flask import render_template, request
from flask_babel import gettext
from atmt import add_to_crawl_list
from manager.call import manager_get_id

conn = account_database_loader()
cursor = conn.cursor()

@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    User = request.cookies.get('USERNAME')
    if User is None:
        User = gettext('Account')

    return render_template(
        '/contribute/index.html',
        User=User
    )

@app.route('/contribute/insert', methods=['GET', 'POST'])
def contribute_insert():
    if request.form.get('add_button') == 'add_clicked':
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_authentication(cursor, username, password, False)

        if username is None or password is None or login is None:
            message_call = "Unable to verify user, looks like you are not logged in to your account, please log in to take any action on the database."
        else:
            url = request.form.get('url')
            message_call = add_to_crawl_list(url)
        
        User = request.cookies.get('USERNAME')
        if User is None:
            User = gettext('Account')

        return render_template(
            '/contribute/index.html',
            User=User,
            message=gettext(message_call)
        )

@app.route('/contribute/change', methods=['GET', 'POST'])
def contribute_change():
    if request.form.get('edit_button') == 'edit_clicked':
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_authentication(cursor, username, password, False)

        if username is None or password is None or login is None:
            message_call = "Unable to verify user, looks like you are not logged in to your account, please log in to take any action on the database."
        else:
            url = request.form.get('url')
            message_call = add_to_crawl_list(url)
        
        User = request.cookies.get('USERNAME')
        if User is None:
            User = gettext('Account')

        return render_template(
            '/contribute/index.html',
            User=User,
            message=gettext(message_call)
        )

@app.route('/contribute/remove', methods=['GET', 'POST'])
def contribute_remove():
    if request.form.get('remove_button') == 'remove_clicked':
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_authentication(cursor, username, password, False)

        if username is None or password is None or login is None:
            message_call = "Unable to verify user, looks like you are not logged in to your account, please log in to take any action on the database."
        else:
            url = request.form.get('url')
            message_call = add_to_crawl_list(url)

        User = request.cookies.get('USERNAME')
        if User is None:
            User = gettext('Account')

        return render_template(
            '/contribute/index.html',
            User=User,
            message=gettext(message_call)
        )

@app.route('/contribute/getid', methods=['GET', 'POST'])
def contribute_getid():
    if request.form.get('find_button') == 'find_clicked':
        url = request.form.get('url')
        type = request.form.get('type')
        message_call=manager_get_id(type, url)

        User = request.cookies.get('USERNAME')
        if User is None:
            User = gettext('Account')

        return render_template(
            '/contribute/index.html',
            User=User,
            message=gettext(message_call)
        )
