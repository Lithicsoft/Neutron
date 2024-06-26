import hashlib
import os
import random
import re
from dotenv import load_dotenv
import dotenv
import requests
from account.authentication import add_user, check_existing_email, check_existing_username, get_user_authentication, update_password, verification
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from account.userid import get_user_id
from app import app, databases
from flask import make_response, redirect, render_template, request
from flask_babel import gettext

conn = databases.account_conn
cursor = conn.cursor()

dotenv.load_dotenv()

def send_email(subject, from_email, to_email, content):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content)

    load_dotenv()

    try: 
        sg = SendGridAPIClient(os.getenv('SG_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print("Error sending email:", str(e))

def verify_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return False
    else:
        return True

@app.route('/account', methods=['GET', 'POST'])
@app.route('/account/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        if request.form.get('login_button') == 'login_clicked':
            recaptcha_response = request.form.get('g-recaptcha-response')
            data = {
                'secret': os.getenv('RECAPTCHA_SECRET_KEY'),
                'response': recaptcha_response
            }

            req = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = req.json()

            User = request.cookies.get('USERNAME')
            if result['success']:
                username = request.form.get('username')
                password = request.form.get('password')

                login = get_user_authentication(cursor, username, password)

                if User is None:
                    User = gettext('Account')

                if login is not None:
                    resp = make_response(render_template(
                        '/account/login.html',
                        User=User,
                        SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                        message=gettext('Logged in successfully.'),
                        redirect='/account/me'
                    ))
                    password = hashlib.md5(hashlib.sha256(password.encode('utf-8')).hexdigest().encode()).hexdigest()
                    resp.set_cookie('USERNAME', username)
                    resp.set_cookie('PASSWORD', password)
                    return resp
                else:
                    return render_template(
                        '/account/login.html',
                        User=User,
                        SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                        message=gettext('Username or password is incorrect.')
                    )
            else:
                return render_template(
                    '/account/login.html',
                    User=User,
                    SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                    message=gettext('CAPTCHA validation failed.')
                )
    else:
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_authentication(cursor, username, password, False)

        if username is not None or password is not None or login is not None:
            return redirect(
                '/account/me',
            )
        else:
            return render_template(
                '/account/login.html',
                User=gettext("Account"),
                SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY')
            )
    
@app.route('/account/register', methods=['GET', 'POST'])
def account_register():
    confirmcode = request.form.get('confirmcode')
    user_id = request.form.get('userid')

    User = request.cookies.get('USERNAME')
    if User is None:
        User = gettext('Account')

    if confirmcode is not None:
        return render_template(
            'account/register.html',
            User=User,
            SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
            message=gettext(verification(conn, cursor, int(user_id), int(confirmcode)))
        )

    if request.method == 'GET':
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_authentication(cursor, username, password, False)

        if username is None or password is None or login is None:
            return render_template(
                '/account/register.html',
                SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                User=User
            )
        else:
            return redirect(
                '/account/login'
            )
    else:
        if request.form.get('register_button') == 'register_clicked':
            recaptcha_response = request.form.get('g-recaptcha-response')
            data = {
                'secret': os.getenv('RECAPTCHA_SECRET_KEY'),
                'response': recaptcha_response
            }

            req = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = req.json()

            if not result['success']:
                return render_template(
                    '/account/register.html',
                    User=User,
                    SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                    message=gettext('CAPTCHA validation failed.')
                )
            else:
                email = request.form.get('email')
                username = request.form.get('username')
                password = request.form.get('password')

                if check_existing_email(cursor, email):
                    return render_template(
                        '/account/register.html',
                        User=User,
                        SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                        message=gettext('This email is already registered. Please use a different email.')
                    )
                elif verify_email(email):
                    return render_template(
                        '/account/register.html',
                        User=User,
                        SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                        message=gettext('This email is invalid, please check again.')
                    )
                elif check_existing_username(cursor, username):
                    return render_template(
                        '/account/register.html',
                        User=User,
                        SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                        message=gettext('This user name already in use. Please use another username.')
                    )
                else:
                    confirm_code = random.randint(10000, 99999)
                    add_user(conn, cursor, email, username, password, confirm_code)
                    user_id = get_user_id(cursor, username)
                    send_email('Neutron Verification', 'lithicsoft@gmail.com', email, 'Hello ' + username + ', Your Neutron confirmation code is: ' + str(confirm_code) + ' and your id is: ' + str(user_id) + '.')
                    return render_template(
                        '/account/register.html',
                        User=User,
                        message=gettext('An email containing a confirmation code and user id has been sent to your account.')
                    )

@app.route('/account/me', methods=['GET', 'POST'])
def myaccount_form():
    if request.method == 'GET':
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_authentication(cursor, username, password, False)

        if username is None or password is None or login is None:
            return redirect(
                '/account/login',
            )
        else:
            return render_template(
                '/account/me.html',
                User=username,
                SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                username=username
            )
    else:
        if request.form.get('change_button') == 'change_clicked':
            recaptcha_response = request.form.get('g-recaptcha-response')
            data = {
                'secret': os.getenv('RECAPTCHA_SECRET_KEY'),
                'response': recaptcha_response
            }

            req = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = req.json()

            if result['success']:
                old_password = request.form.get('oldpassword')
                new_password = request.form.get('newpassword')
                username = request.cookies.get('USERNAME')

                login = get_user_authentication(cursor, username, old_password)

                if login is not None:
                    user_id = get_user_id(cursor, username)
                    update_password(conn, cursor, user_id, new_password)

                    User = request.cookies.get('USERNAME')
                    if User is None:
                        User = gettext('Account')

                    resp = make_response(render_template(
                        '/account/me.html',
                        User=User,
                        SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                        message=gettext('Changed password successfully.')
                    ))

                    resp.set_cookie('USERNAME', '', expires=0)
                    resp.set_cookie('PASSWORD', '', expires=0)

                    return resp
                else:
                    return render_template(
                        '/account/me.html',
                        User=User,
                        username=User,
                        SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                        message=gettext('Password and username are incorrect, please try again.')
                    )
            else:
                return render_template(
                    '/account/me.html',
                    User=User,
                    username=User,
                    SITE_KEY=os.getenv('RECAPTCHA_SITE_KEY'),
                    message=gettext('CAPTCHA validation failed.')
                )

@app.route('/account/me/logout', methods=['GET', 'POST'])
def myaccount_logout():
    username = request.cookies.get('USERNAME')
    password = request.cookies.get('PASSWORD')

    User = request.cookies.get('USERNAME')
    if User is None:
        User = gettext('Account')

    if username is None or password is None:
        return redirect(
            '/account/login'
        )
    else:
        resp = make_response(redirect(
                    '/account/login'
                ))
        resp.set_cookie('USERNAME', '', expires=0)
        resp.set_cookie('PASSWORD', '', expires=0)

        return resp