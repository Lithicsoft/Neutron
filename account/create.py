import smtplib
import time
import streamlit as st
from account.loader import account_database_loader

conn = account_database_loader()
cursor = conn.cursor()

def add_user(email, username, password):
    cursor.execute('''INSERT INTO users (email, username, password) VALUES (?, ?, ?)''', (email, username, password))
    conn.commit()

def check_existing_email(email):
    cursor.execute("SELECT * FROM users WHERE email=?", (email,))
    return cursor.fetchone() is not None

def check_existing_username(username):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    return cursor.fetchone() is not None

st.title('User Registration')

email = st.text_input('Email:')
username = st.text_input('Username:')
password = st.text_input('Password:', type='password')
confirm_button = st.button('Register')

if confirm_button:
    if check_existing_email(email):
        st.error('This email is already registered. Please use a different email.')
    elif check_existing_username(username):
        st.error('This user name already in use. Please use another username.')
    else:
        with st.spinner('Checking the given information...'):
            time.sleep(1)
            add_user(email, username, password)
            st.success('Your account has been successfully created.')
