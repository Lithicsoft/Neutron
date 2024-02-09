import streamlit as st
import time
from initializer.loader import database_loader
from manager.manager import *
from search.index import Search_Data

conn = database_loader()

st.title('MonoSearch')

st.session_state.setdefault('form_state', True)

Search_Result = []

with st.form('Input_Form'):
    col1, col2, col3, col4, col5 = st.columns([3, 0.8, 0.6, 0.6, 0.8])
    AForm = st.session_state.form_state

    with col1:
        keyword = st.text_input('Try to search something!', placeholder='Try to search something!', label_visibility='collapsed')
    
    with col2:
        submitted1 = st.form_submit_button('Search')

    with col3:
        submitted2 = st.form_submit_button('Add')

    with col4:
        submitted3 = st.form_submit_button('Edit')

    with col5:
        submitted4 = st.form_submit_button('Remove')

    if keyword and submitted1:
        Search_Result = Search_Data(conn, keyword)

    if submitted2 and AForm == True:
        username = st.text_input('Username: ')
        password = st.text_input('Password: ', type='password')

        link = st.text_input('Link (Should not contain a "/" at the end, use only "http" and "https"): ')
        title = st.text_input('Title: ')
        text = st.text_input('Text: ')
        description = st.text_input('Description: ')
        keywords = st.text_input('Keywords: ')
        shorttext = st.text_input('Short Text: ')

        if username and password and link and title and text and description and keywords and shorttext:
            with st.spinner('Checking the given information...'):
                time.sleep(1)
                manager_insert_data(conn, username, password, link, title, text, description, keywords, shorttext)
                st.session_state.add_state = False
    elif submitted2 and not AForm:
        st.session_state.add_state = True

    if submitted3 and AForm == True:
        username = st.text_input('Username: ')
        password = st.text_input('Password: ', type='password')

        site_id = st.text_input('Site ID: ')
        link = st.text_input('Link (Should not contain a "/" at the end, use only "http" and "https"): ')
        title = st.text_input('Title: ')
        text = st.text_input('Text: ')
        description = st.text_input('Description: ')
        keywords = st.text_input('Keywords: ')
        shorttext = st.text_input('Short Text: ')

        if username and password and site_id and link and title and text and description and keywords and shorttext:
            with st.spinner('Checking the given information...'):
                time.sleep(1)
                manager_edit_data(conn, username, password, site_id, link, title, text, description, keywords, shorttext)
                st.session_state.add_state = False
    elif submitted3 and not AForm:
        st.session_state.add_state = True

    if submitted4 and AForm == True:
        username = st.text_input('Username: ')
        password = st.text_input('Password: ', type='password')

        site_id = st.text_input('Site ID: ')
        
        if username and password and site_id:
            with st.spinner('Checking the given information...'):
                time.sleep(1)
                manager_remove_data(conn, username, password, site_id)
                st.session_state.add_state = False
    elif submitted4 and not AForm:
        st.session_state.add_state = True

for row in Search_Result:
    st.markdown('```' + str(row[0]) + '``` ```' + row[1] + '```')
    st.markdown("### [" + row[2] + ']' + '(' + row[1] + ')')
    st.write(row[6])
    st.markdown("&nbsp;&nbsp;&nbsp;")
