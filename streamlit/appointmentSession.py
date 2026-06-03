import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
st.title('📆 Appointment Booking and Cost Calculator')
if "bookings" not in st.session_state:
	st.session_state.bookings = []
today = datetime.date.today()
end_date = today + relativedelta(months=+6)
date = st.date_input('Select appointment date', min_value=today, max_value=end_date, value=None, key=None)
time = st.time_input('Select appointment time', value=datetime.time(9, 0), step=datetime.timedelta(hours=1))
service = st.selectbox('Select service', options=['Consultation', 'Premium', 'Emergency'])
duration= st.number_input('Enter duration of appointment (in hours)', min_value=1, max_value=8, step=1)

pricing = {
		'Consultation': 500,
		'Premium': 1000,
		'Emergency': 1500
}
total_cost = pricing[service] * duration

success = st.button('Book Appointment')
if success:
	st.success('✅ Appointment booked successfully!')
	bookingdata= {
		'date': date,
		'time': time,
		'service': service,
		'duration': duration,
		'total_cost': total_cost
	}
	st.session_state.bookings.append(bookingdata)
	st.subheader('📋 Appointment Details')
	if st.session_state.bookings:
		for idx, booking in enumerate(st.session_state.bookings):
			st.write(f'### Appointment {idx + 1}')
			st.write(f'📅 Date: {booking["date"]}')
			st.write(f'🕐 Time: {booking["time"]}')
			st.write(f'💇 Service: {booking["service"]}')
			st.write(f'🕒 Duration: {booking["duration"]} hours')
			st.info(f'💶 Total cost of appointment: {booking["total_cost"]}')