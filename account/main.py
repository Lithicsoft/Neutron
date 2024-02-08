import smtplib
import time
import streamlit as st
from account.loader import account_database_loader
from account.reliability import get_user_reliability
from account.userid import get_user_id
from account.username import get_username
from log.write import sys_log

conn = account_database_loader()
cursor = conn.cursor()

def add_user(email, username, password):
    cursor.execute('''INSERT INTO users (email, username, password) VALUES (?, ?, ?)''', (email, username, password))
    sys_log("Created User Account", "Username: " + username + " Email: " + email + " Password: " + password)
    conn.commit()

def update_password(user_id, email, new_password):
    cursor.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user_id))
    sys_log("Changed User Password", "Username: " + username + " User ID: " + str(user_id) + " Email: " + email + " Password: " + password)
    conn.commit()

def update_username(user_id, email, new_username):
    cursor.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user_id))
    sys_log("Changed Username", "Username: " + username + " User ID: " + str(user_id) + " Email: " + email + " Password: " + password)
    conn.commit()

def check_existing_email(email):
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    return cursor.fetchone() is not None

def check_existing_username(username):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    return cursor.fetchone() is not None

st.title('Account Manager')

st.session_state.setdefault('form_state', True)
AForm = st.session_state.form_state

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

            if email and username and password:
                if check_existing_email(email):
                    st.error('This email is already registered. Please use a different email.')
                elif check_existing_username(username):
                    st.error('This user name already in use. Please use another username.')
                else:
                    with st.spinner('Checking the given information...'):
                        add_user(email, username, password)
                        time.sleep(1)
                        st.success('Your account has been successfully created.')
        
        if submitted2:
            email = st.text_input('Email: ')
            username = st.text_input('Username: ')
            password = st.text_input('Password: ', type='password')

            st.markdown('---')

            if get_user_reliability(cursor, username, password) is not None:
                user_id = get_user_id(cursor, username)
                new_username = st.text_input('New Username: ')
                new_password = st.text_input('New Password: ', type='password')
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
                st.write("User ID: " + str(get_user_id(cursor, username)))
            elif user_id and not username:
                st.write("Username: " + get_username(cursor, user_id))

    else:
        open_button = st.form_submit_button('Open Form')
        if open_button:
            st.session_state.form_state = True

    