import streamlit as st
def add_numbers(num1, num2):
		st.session_state.sum = num1 + num2
		st.write('Result:', args)
num1 = st.number_input('Enter first number', min_value=0, max_value=100, step=1)
num2 = st.number_input('Enter second number', min_value=0, max_value=100, step=1)
st.button('Add', on_click=add_numbers, args=(10,12))