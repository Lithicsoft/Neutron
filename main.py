import streamlit as st
import time

from initializer.loader import database_loader
from manager.insert import insert_data
from search.index import Search_Data
from initializer.database import Initializer_Database

Initializer_Database()

conn = database_loader()

st.title('MonoSearch')

st.session_state.setdefault('add_state', True)

with st.form('Input_Form'):
    col1, col2, col3 = st.columns([3, 0.6, 0.4])
    AddForm = st.session_state.add_state

    with col1:
        keyword = st.text_input('Try to search something!', value='Try to search something!', placeholder='Try to search something!', label_visibility='collapsed')
    
    with col2:
        submitted1 = st.form_submit_button('Search')

    with col3:
        submitted2 = st.form_submit_button('Add')

    if keyword and submitted1:
        Search_Data(conn, keyword)

    if submitted2 and AddForm == True:
        link = st.text_input('Link (Should not contain a "/" at the end, use only "http" and "https"): ')
        title = st.text_input('Title: ')
        text = st.text_input('Text: ')
        description = st.text_input('Description: ')
        keywords = st.text_input('Keywords: ')
        shorttext = st.text_input('Short Text: ')

        if link and title and text and description and keywords and shorttext:
            with st.spinner('Checking the given information...'):
                time.sleep(1)
                insert_data(conn, link, title, text, description, keywords, shorttext)
                st.session_state.add_state = False
    elif submitted2 and not AddForm:
        st.session_state.add_state = True
        