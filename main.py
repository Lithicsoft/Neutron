import streamlit as st

from manager.insert import insert_data
from search.index import Search_Data
from initializer.database import Initializer_Database

Initializer_Database()

st.title('MonoSearch')

st.session_state.setdefault('add_state', False)

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
        Search_Data(keyword)

    if submitted2 and AddForm == True:
        name = st.text_input('Enter website name:')
        address = st.text_input('Enter website address:')
        
        if name and address:
            insert_data(name, address)
            st.success('Data inserted successfully!')
            st.session_state.add_state = False
    elif submitted2 and not AddForm:
        st.session_state.add_state = True
        