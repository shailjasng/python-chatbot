import streamlit as st
import datetime

option = st.selectbox('Select your gender', options=['choose your gender','Male', 'Female', 'Other'])
if option != 'choose your gender':
  st.write('you selected:', option)
options = st.multiselect('Select your favorite colors', options=['Red', 'Green', 'Blue', 'Yellow'], default=['Red', 'Green'])
st.write('You selected:', options)
agree = st.checkbox('I agree to the terms and conditions')
st.write('You agreed:', agree)
transportation = st.radio('Select your preferred mode of transportation', options=['Car', 'Bike', 'Public Transport'])
st.write('You selected:', transportation)
ageSlider = st.slider('Select your age', min_value=0, max_value=100, step=1)
if ageSlider < 18:
		st.write('You are a minor.')
else:
		st.write('You are an adult.')
name = st.text_input('Enter your name')
st.write('You entered:', name)
dob = st.date_input('Select your date of birth', min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2026, 12, 31), value=None, key=None)
st.write('You selected:', dob)