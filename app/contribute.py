import os
import dotenv
import requests
from account.authentication import get_user_authentication
from app import app, databases
from flask import render_template, request
from flask_babel import gettext
from crawl import add_to_crawl_list

conn = databases.account_conn
cursor = conn.cursor()

dotenv.load_dotenv()

@app.route('/contribute', methods=['GET', 'POST'])
def contribute():
    User = request.cookies.get('USERNAME')
    if User is None:
        User = gettext('Account')

    return render_template(
        '/contribute/index.html',
        SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
        User=User
    )

@app.route('/contribute/crawl', methods=['GET', 'POST'])
def contribute_insert():
    if request.form.get('submit_button') == 'submit_clicked':
        recaptcha_response = request.form.get('g-recaptcha-response')
        data = {
            'secret': os.getenv('RECAPTCHA_SECRET_KEY'),
            'response': recaptcha_response
        }

        req = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = req.json()

        User = request.cookies.get('USERNAME')
        if result['success']:
            username = request.cookies.get('USERNAME')
            password = request.cookies.get('PASSWORD')

            login = get_user_authentication(cursor, username, password, False)

            if username is None or password is None or login is None:
                message_call = "Unable to verify user, looks like you are not logged in to your account, please log in to take any action on the database."
            else:
                url = request.form.get('url')
                message_call = add_to_crawl_list(url)
            
            if User is None:
                User = gettext('Account')

            return render_template(
                '/contribute/index.html',
                User=User,
                SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                message=gettext(message_call)
            )
        else:
            return render_template(
                '/contribute/index.html',
                User=User,
                SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                message=gettext('CAPTCHA validation failed.')
            )