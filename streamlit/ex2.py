import streamlit as st

st.write('hello world')
st.image('https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png')
st.image("images/download.jpg", caption="Tiger")
name = st.text_input('Enter your name', placeholder='Type your name here')
st.markdown(f"Hello, {name}!")