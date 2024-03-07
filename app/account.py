import hashlib
import os
import random
import re
from account.loader import account_database_loader
from account.reliability import get_user_reliability
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from account.userid import get_user_id
from app import app
from flask import make_response, redirect, render_template, request

from log.write import sys_log

conn = account_database_loader()
cursor = conn.cursor()

def send_email(subject, from_email, to_email, content):
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content)

    try:
        sg = SendGridAPIClient(os.environ.get('SG_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print("Error sending email:", str(e))

def add_user(email, username, password, confirm):
    password = hashlib.md5(hashlib.sha256(password.encode('utf-8')).hexdigest().encode()).hexdigest()
    cursor.execute('''INSERT INTO users (email, username, password, confirm) VALUES (%s, %s, %s, %s)''', (email, username, password, confirm))
    sys_log("Created User Account", "Username: " + username + " Email: " + email)
    conn.commit()

def update_password(user_id, username, email, new_password):
    new_password = hashlib.md5(hashlib.sha256(new_password.encode('utf-8')).hexdigest().encode()).hexdigest()
    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
    sys_log("Changed User Password", "Username: " + username + " User ID: " + str(user_id) + " Email: " + email)
    conn.commit()

def verify_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return False
    else:
        return True

def check_existing_email(email):
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    return cursor.fetchone() is not None

def check_existing_username(username):
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    return cursor.fetchone() is not None

def verification(user_id, confirmation_code):
    cursor.execute("SELECT confirm FROM users WHERE id = %s", (user_id,))
    confirm_value = cursor.fetchall()[0][0]
    if int(confirmation_code) == confirm_value:
        cursor.execute("UPDATE users SET confirm = 0 WHERE id = %s", (user_id,))
        cursor.execute("UPDATE users SET reliability = 0 WHERE id = %s", (user_id,))
        conn.commit()
        return 'Your account has been successfully created.'
    else:
        return 'The verification code is incorrect, please check again.'

@app.route('/account', methods=['GET', 'POST'])
@app.route('/account/login', methods=['GET', 'POST'])
def login_form():
    if request.method == 'POST':
        if request.form.get('login_button') == 'login_clicked':
            username = request.form.get('username')
            password = request.form.get('password')

            login = get_user_reliability(cursor, username, password)

            if login is not None:
                resp = make_response(render_template(
                    '/account/login.html',
                    message='Logged in successfully.',
                    redirect='/account/me'
                ))
                password = hashlib.md5(hashlib.sha256(password.encode('utf-8')).hexdigest().encode()).hexdigest()
                resp.set_cookie('USERNAME', username)
                resp.set_cookie('PASSWORD', password)
                return resp
            else:
                return render_template(
                    '/account/login.html',
                    message='Account does not exist.'
                )
    else:
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_reliability(cursor, username, password, False)

        if username is not None or password is not None or login is not None:
            return redirect(
                '/account/me'
            )
        else:
            return render_template(
                '/account/login.html'
            )
    
@app.route('/account/register', methods=['GET', 'POST'])
def account_register():
    confirmcode = request.form.get('confirmcode')
    user_id = request.form.get('userid')
    if confirmcode is not None:
        return render_template(
            'account/register.html',
            message=verification(int(user_id), int(confirmcode))
        )

    if request.method == 'GET':
        return render_template(
            '/account/register.html'
        )
    else:
        if request.form.get('register_button') == 'register_clicked':
            email = request.form.get('email')
            username = request.form.get('username')
            password = request.form.get('password')

            if check_existing_email(email):
                return render_template(
                    '/account/register.html',
                    message='This email is already registered. Please use a different email.'
                )
            elif verify_email(email):
                return render_template(
                    '/account/register.html',
                    message='This email is invalid, please check again.'
                )
            elif check_existing_username(username):
                return render_template(
                    '/account/register.html',
                    message='This user name already in use. Please use another username.'
                )
            else:
                confirm_code = random.randint(10000, 99999)
                add_user(email, username, password, confirm_code)
                user_id = get_user_id(cursor, username)
                add_user(email, username, password, confirm_code)
                send_email('Neutron Verification', 'lithicsoft@gmail.com', email, 'Hello ' + username + ', Your Neutron confirmation code is: ' + str(confirm_code) + ' and your id is: ' + str(user_id) + '.')
                return render_template(
                    '/account/register.html',
                    message='An email containing a confirmation code and user id has been sent to your account.'
                )

@app.route('/account/me', methods=['GET', 'POST'])
def myaccount_form():
    if request.method == 'GET':
        username = request.cookies.get('USERNAME')
        password = request.cookies.get('PASSWORD')

        login = get_user_reliability(cursor, username, password, False)

        if username is None or password is None or login is None:
            return redirect(
                '/account/login'
            )
        else:
            return render_template(
                '/account/me.html',
                username=username
            )
    
@app.route('/account/me/logout', methods=['GET', 'POST'])
def myaccount_logout():
    username = request.cookies.get('USERNAME')
    password = request.cookies.get('PASSWORD')

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