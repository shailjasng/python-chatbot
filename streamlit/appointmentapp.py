import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
st.title('📆 Appointment Booking and Cost Calculator')
today = datetime.date.today()
end_date = today + relativedelta(months=+6)
date = st.date_input('Select appointment date', min_value=today, max_value=end_date, value=None, key=None)
time = st.time_input('Select appointment time', value=datetime.time(9, 0), step=datetime.timedelta(hours=1))
service = st.selectbox('Select service', options=['Consultation', 'Premium', 'Emergency'])
duration= st.number_input('Enter duration of appointment (in hours)', min_value=1, max_value=8, step=1)
#cost = 0
# if service == 'Consultation':
# 		cost = 500
# elif service == 'Premium':
# 		cost = 1000
# elif service == 'Emergency':
# 		cost = 1500
# total_cost = cost * duration
# st.write('💶Total cost of appointment:', total_cost)
pricing = {
		'Consultation': 500,
		'Premium': 1000,
		'Emergency': 1500
}
total_cost = pricing[service] * duration
st.info(f'💶 Total cost of appointment: {total_cost}')
success = st.button('Book Appointment')
if success:
		st.success('✅ Appointment booked successfully!')
		st.write(f'📅 Date: {date}')
		st.write(f'🕐 Time: {time}')
		st.write(f'💇 Service: {service}')
		st.write(f'🕒 Duration: {duration} hours')