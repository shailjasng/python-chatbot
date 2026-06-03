import streamlit as st
num1 = st.number_input('Number 1:')
num2 = st.number_input('Number 2:')
if st.button('Add'):
    st.write('Result:', num1 + num2)