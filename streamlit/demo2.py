import streamlit as st

if 'name_input' not in st.session_state:
		st.session_state.name_input = ''
st.text_input('Enter your name', placeholder='Type your name here' ,
							key='name_input')
#st.session_state.name_input = st.session_state.name_input or ''
st.markdown(f"Hello, {st.session_state.name_input}!")

