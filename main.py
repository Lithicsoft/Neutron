from datetime import datetime
import streamlit as st
import time
import wikipedia
from typing import List
from langdetect import detect
from streamlit_searchbox import st_searchbox
from initializer.loader import database_loader
from manager.manager import *
from search.index import Search_Data
from search.safe import return_special_characters

if 'config' not in st.session_state:
    st.session_state.config = st.set_page_config(
    page_title="Neutron Search",
    page_icon="🔎",
)

if 'conn0' not in st.session_state:
    st.session_state.conn0 = database_loader(0)
conn0 = st.session_state.conn0

if 'conn1' not in st.session_state:
    st.session_state.conn1 = database_loader(1)
conn1 = st.session_state.conn1

if 'conn2' not in st.session_state:
    st.session_state.conn2 = database_loader(2)
conn2 = st.session_state.conn2

def search_suggestion(searchterm: str) -> List[any]:
    return wikipedia.search(searchterm) if searchterm else []

st.title('Neutron')

st.session_state.setdefault('form_state', True)
Search_Result = []

with st.form('Input_Form'):
    col1, col2, col3, col4, col5 = st.columns([3, 1.4, 1.1, 1.5, 1.2])
    AForm = st.session_state.form_state

    with col1:
        keyword = st_searchbox(search_suggestion, placeholder='Try to search something!')
    with col2:
        submitted1 = st.form_submit_button('Search')
        options_types = ['Text', 'Image', 'Video']
        search_type = st.selectbox('Type:', options_types, index=0)
    with col3:
        submitted2 = st.form_submit_button('Insert')    
        options_language = ['all', 'af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa', 'fi', 'fr', 'gu', 'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'so', 'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'zh-cn', 'zh-tw']
        search_language = st.selectbox('Language:', options_language)
    with col4:
        submitted3 = st.form_submit_button('Edit')
        search_time = st.date_input('Time', value=None)
    with col5:
        submitted4 = st.form_submit_button('Remove')

    if search_type == 'Text':
        conn = conn0
    elif search_type == 'Image':
        conn = conn1
    elif search_type == 'Video':
        conn = conn2 

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

#####

if search_type == 'Text':
    if Search_Result is None:
        st.write("No results found.")
    else:
        if search_language == 'all':
            if search_time is None:
                for row in Search_Result:
                    row2 = return_special_characters(row[2])
                    row6 = return_special_characters(row[6])
                    row_title = row2.replace('\n', ' ')
                    row_title = row_title.replace(':', ' ')
                    row_shorttext = row6.replace('\n', ' ')
                    row_shorttext = row_shorttext.replace('```', ' ')
                    st.markdown("### [" + row_title + ']' + '(' + row[1] + ') ' + '```' + str(row[0]) + '```')
                    st.markdown(row_shorttext)
                    st.markdown("   ")
            else:
                for row in Search_Result:
                    dt_object = datetime.strptime(row[7], "%Y-%m-%d").date()
                    print(dt_object, " - ", search_time)
                    if dt_object >= search_time:
                        row2 = return_special_characters(row[2])
                        row6 = return_special_characters(row[6])
                        row_title = row2.replace('\n', ' ')
                        row_title = row_title.replace(':', ' ')
                        row_shorttext = row6.replace('\n', ' ')
                        row_shorttext = row_shorttext.replace('```', ' ')
                        st.markdown("### [" + row_title + ']' + '(' + row[1] + ') ' + '```' + str(row[0]) + '```')
                        st.markdown(row_shorttext)
                        st.markdown("   ")
        else:
            for row in Search_Result:
                if detect(row[2]) == search_language or detect(row[6]) == search_language:
                    if search_time is None:
                        row2 = return_special_characters(row[2])
                        row6 = return_special_characters(row[6])
                        row_title = row2.replace('\n', ' ')
                        row_title = row_title.replace(':', ' ')
                        row_shorttext = row6.replace('\n', ' ')
                        row_shorttext = row_shorttext.replace('```', ' ')
                        st.markdown("### [" + row_title + ']' + '(' + row[1] + ') ' + '```' + str(row[0]) + '```')
                        st.markdown(row_shorttext)
                        st.markdown("   ")
                    else:
                        dt_object = datetime.strptime(row[7], "%Y-%m-%d").date()
                        if dt_object >= search_time:
                            row2 = return_special_characters(row[2])
                            row6 = return_special_characters(row[6])
                            row_title = row2.replace('\n', ' ')
                            row_title = row_title.replace(':', ' ')
                            row_shorttext = row6.replace('\n', ' ')
                            row_shorttext = row_shorttext.replace('```', ' ')
                            st.markdown("### [" + row_title + ']' + '(' + row[1] + ') ' + '```' + str(row[0]) + '```')
                            st.markdown(row_shorttext)
                            st.markdown("   ")
elif search_type == 'Image':
    if Search_Result is None:
        st.write("No results found.")
    else:
        if search_language == 'all':
            if search_time is None:
                for i in range(0, len(Search_Result), 2):
                    cols = st.columns(2)
                    for j in range(2):
                        if i + j < len(Search_Result):
                            row = Search_Result[i + j]
                            cols[j].image(image=row[1])
                            row2 = return_special_characters(row[2])
                            row_title = row2.replace('\n', ' ')
                            row_title = row_title.replace(':', ' ')
                            cols[j].markdown("### [" + row_title + ']' + '(' + row[1] + ')' + '```' + str(row[0]) + '```')
                            cols[j].markdown(row[4])
                            cols[j].markdown("   ")
            else:
                for i in range(0, len(Search_Result), 2):
                    cols = st.columns(2)
                    for j in range(2):
                        if i + j < len(Search_Result):
                            row = Search_Result[i + j]
                            dt_object = datetime.strptime(row[7], "%Y-%m-%d").date()
                            if dt_object >= search_time:
                                cols[j].image(image=row[1])
                                row2 = return_special_characters(row[2])
                                row_title = row2.replace('\n', ' ')
                                row_title = row_title.replace(':', ' ')
                                cols[j].markdown("### [" + row_title + ']' + '(' + row[1] + ')' + '```' + str(row[0]) + '```')
                                cols[j].markdown(row[4])
                                cols[j].markdown("   ")
        else:
            if search_time is None:
                for i in range(0, len(Search_Result), 2):
                    if detect(row[2]) == search_language:
                        cols = st.columns(2)
                        for j in range(2):
                            if i + j < len(Search_Result):
                                row = Search_Result[i + j]
                                cols[j].image(image=row[1])
                                row2 = return_special_characters(row[2])
                                row_title = row2.replace('\n', ' ')
                                row_title = row_title.replace(':', ' ')
                                cols[j].markdown("### [" + row_title + ']' + '(' + row[1] + ')' + '```' + str(row[0]) + '```')
                                cols[j].markdown(row[4])
                                cols[j].markdown("   ")
            else:
                for i in range(0, len(Search_Result), 2):
                    if detect(row[2]) == search_language:
                        cols = st.columns(2)
                        for j in range(2):
                            if i + j < len(Search_Result):
                                row = Search_Result[i + j]
                                dt_object = datetime.strptime(row[7], "%Y-%m-%d").date()
                                if dt_object >= search_time:
                                    cols[j].image(image=row[1])
                                    row2 = return_special_characters(row[2])
                                    row_title = row2.replace('\n', ' ')
                                    row_title = row_title.replace(':', ' ')
                                    cols[j].markdown("### [" + row_title + ']' + '(' + row[1] + ')' + '```' + str(row[0]) + '```')
                                    cols[j].markdown(row[4])
                                    cols[j].markdown("   ")
elif search_type == 'Video':
    if Search_Result is None:
        st.write("No results found.")
    else:
        if search_language == 'all':
            if search_time is None:
                for row in Search_Result:
                    col1, col2 = st.columns([1, 3])
                    col1.video(row[1])
                    row2 = return_special_characters(row[2])
                    row_title = row2.replace('\n', ' ')
                    row_title = row_title.replace(':', ' ')
                    col2.markdown('```' + str(row[0]) + '``` ```' + row[1] + '```')
                    col2.markdown("### [" + row_title + ']' + '(' + row[1] + ')')
                    col2.markdown(row[7])
                    st.markdown("   ")
            else:
                for row in Search_Result:
                    dt_object = datetime.strptime(row[7], "%Y-%m-%d").date()
                    if dt_object >= search_time:
                        col1, col2 = st.columns([1, 3])
                        col1.video(row[1])
                        row2 = return_special_characters(row[2])
                        row_title = row2.replace('\n', ' ')
                        row_title = row_title.replace(':', ' ')
                        col2.markdown('```' + str(row[0]) + '``` ```' + row[1] + '```')
                        col2.markdown("### [" + row_title + ']' + '(' + row[1] + ')')
                        col2.markdown(row[7])
                        st.markdown("   ")
        else:
            for row in Search_Result:
                if detect(row[2]) == search_language:
                    if search_time is None:
                        col1, col2 = st.columns([1, 3])
                        col1.video(row[1])
                        row2 = return_special_characters(row[2])
                        row_title = row2.replace('\n', ' ')
                        row_title = row_title.replace(':', ' ')
                        col2.markdown('```' + str(row[0]) + '``` ```' + row[1] + '```')
                        col2.markdown("### [" + row_title + ']' + '(' + row[1] + ')')
                        col2.markdown(row[7])
                        st.markdown("   ")
                    else:
                        dt_object = datetime.strptime(row[7], "%Y-%m-%d").date()
                        if dt_object >= search_time:
                            col1, col2 = st.columns([1, 3])
                            col1.video(row[1])
                            row2 = return_special_characters(row[2])
                            row_title = row2.replace('\n', ' ')
                            row_title = row_title.replace(':', ' ')
                            col2.markdown('```' + str(row[0]) + '``` ```' + row[1] + '```')
                            col2.markdown("### [" + row_title + ']' + '(' + row[1] + ')')
                            col2.markdown(row[7])
                            st.markdown("   ")
