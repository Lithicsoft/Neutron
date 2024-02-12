import re
import os
import time
import random
import streamlit as st
from hashlib import sha256
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from account.loader import account_database_loader
from account.reliability import get_user_reliability
from account.userid import get_user_id
from account.username import get_username
from log.write import sys_log

st.set_page_config(
    page_title="Neutron Account",
    page_icon="👤",
)

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
    password = sha256(password.encode('utf-8')).hexdigest()
    cursor.execute('''INSERT INTO users (email, username, password, confirm) VALUES (?, ?, ?, ?)''', (email, username, password, confirm))
    sys_log("Created User Account", "Username: " + username + " Email: " + email)
    conn.commit()

def update_password(user_id, email, new_password):
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
    sys_log("Changed User Password", "Username: " + username + " User ID: " + str(user_id) + " Email: " + email)
    conn.commit()

def update_username(user_id, email, new_username):
    cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
    sys_log("Changed Username", "Username: " + username + " User ID: " + str(user_id) + " Email: " + email)
    conn.commit()

def verify_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return False
    else:
        return True

def check_existing_email(email):
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    return cursor.fetchone() is not None

def check_existing_username(username):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    return cursor.fetchone() is not None

def verification(user_id, confirmation_code, confirm_value):
    if int(confirmation_code) == confirm_value:
        cursor.execute("UPDATE users SET confirm = 0 WHERE id = ?", (user_id,))
        cursor.execute("UPDATE users SET reliability = 0 WHERE id = ?", (user_id,))
        conn.commit()
        st.success('Your account has been successfully created.')

        st.session_state.email_input = False
        st.session_state.username_input = False
        st.session_state.password_input = False
        st.session_state.confirm_code_input = True
        st.session_state.create_state = True
    else:
        st.error('The verification code is incorrect, please check again.')
    
st.title('Account Manager')

st.session_state.setdefault('form_state', True)
st.session_state.setdefault('create_state', True)
AForm = st.session_state.form_state

st.session_state.setdefault('confirm_value', 0)
st.session_state.setdefault('confirmation_code', 0)

with st.form(key = 'Account_Form'):
    col1, col2, col3 = st.columns([0.1, 0.1, 0.1])

    if AForm:
        with col1:
            submitted1 = st.form_submit_button('Create')
        with col2:
            submitted2 = st.form_submit_button('Change')
        with col3:
            submitted3 = st.form_submit_button('Find')

        if submitted1:
            email = st.text_input('Email:')
            username = st.text_input('Username:')
            password = st.text_input('Password:', type='password')
            confirm_code = st.text_input('Confirmation code:')
            st.session_state.confirmation_code = confirm_code

            if email and username and password:
                if st.session_state.create_state:
                    if check_existing_email(email):
                        st.error('This email is already registered. Please use a different email.')
                    elif verify_email(email):
                        st.error('This email is invalid, please check again.')
                    elif check_existing_username(username):
                        st.error('This user name already in use. Please use another username.')
                    else:
                        with st.spinner('Creating account...'):
                            st.session_state.confirm_value = random.randint(1000, 9999)
                            add_user(email, username, password, st.session_state.confirm_value)
                            send_email('Verification', 'lithicsoft@gmail.com', email, 'Hello ' + username + ', Your Neutron confirmation code is: ' + str(st.session_state.confirm_value))
                            time.sleep(1)
                            st.success('An email containing a confirmation code has been sent to your account.')

                            st.session_state.create_state = False
                else:
                    user_id = get_user_id(cursor, username)
                    verification(user_id, st.session_state.confirmation_code, st.session_state.confirm_value)

            close_button = st.form_submit_button('Close')

            if close_button:
                st.session_state.form_state = False
        
        if submitted2:
            email = st.text_input('Email: ')
            username = st.text_input('Username: ')
            password = st.text_input('Password: ', type='password')

            st.markdown('---')

            if get_user_reliability(cursor, username, password) is not None:
                user_id = get_user_id(cursor, username)
                new_username = st.text_input('New Username:')
                new_password = st.text_input('New Password:', type='password')
                if new_username:
                    update_username(user_id, email, new_username)
                    st.success('Your account username has been successfully updated.')
                if new_password:
                    update_password(user_id, email, new_password)
                    st.success('Your account password has been successfully updated.')
            elif get_user_reliability(cursor, username, password) is None:
                pass
            else:
                st.error("Couldn't find your account, please check again.")

            close_button = st.form_submit_button('Close')

            if close_button:
                st.session_state.form_state = False

        if submitted3:
            username = st.text_input('Username: ')
            user_id = st.text_input('User ID: ')

            st.markdown('---')

            if username and not user_id:
                st.write("User ID:" + str(get_user_id(cursor, username)))
            elif user_id and not username:
                st.write("Username:" + get_username(cursor, user_id))

    else:
        open_button = st.form_submit_button('Open Form')
        if open_button:
            st.session_state.form_state = True

    
