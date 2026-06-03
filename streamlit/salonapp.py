import streamlit as st
import datetime

st.title('💇 Salon Appointment Booking App')
if "appointments" not in st.session_state:
  st.session_state.appointments = []
if "errors" not in st.session_state:
  st.session_state.errors = []
with st.form(key='appointment_form'):
    name = st.text_input('Enter your name')
    services = st.selectbox('Select a service', ['Haircut', 'Hair Coloring', 'Manicure', 'Pedicure'])
    date = st.date_input('Select appointment date', min_value=datetime.date.today())
    selected_time = st.time_input('Select appointment time', value=datetime.time(9, 0), step=datetime.timedelta(minutes=30))
    agreement = st.checkbox('I agree to the terms and conditions')
    submitted = st.form_submit_button('Book Appointment')

if submitted:
    st.session_state.errors.clear()  # Clear previous errors
    if not name.strip():
            st.session_state.errors.append('Please enter your name.')
    if not agreement:
            st.session_state.errors.append('You must agree to the terms and conditions to book an appointment.')
    if selected_time < datetime.time(9, 0) or selected_time > datetime.time(18, 0):
            st.session_state.errors.append('Please select a time between 9:00 AM and 6:00 PM.')
    for idx, existing_appointment in enumerate(st.session_state.appointments):
        if existing_appointment['date'] == date and existing_appointment['time'] ==  selected_time:
                st.session_state.errors.append('The selected time slot is already booked. Please choose a different time.')
                break

    if st.session_state.errors:        
        for error in st.session_state.errors:
            st.error(error)      
    else:
        appointment = {
            'name': name,
            'services': services,
            'date': date,
            'time': selected_time
        }
        st.session_state.appointments.append(appointment)
        st.success('Appointment booked successfully!')
        if st.session_state.appointments:
          for idx, appointment in enumerate(st.session_state.appointments):
            st.subheader("📅 Appointments")
            st.write(f'### Appointment {idx + 1}')
            st.write(f'Name: {appointment["name"]}')
            st.write(f'Service: {appointment["services"]}')
            st.write(f'Date: {appointment["date"]}')
            st.write(f'Time: {appointment["time"]}')