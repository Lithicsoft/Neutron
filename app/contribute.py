from account.authentication import get_user_authentication
from app import app, databases
from flask import render_template, request
from flask_babel import gettext
from crawl import add_to_crawl_list

conn = databases.account_conn
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

@app.route('/contribute/crawl', methods=['GET', 'POST'])
def contribute_insert():
    if request.form.get('submit_button') == 'submit_clicked':
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