import streamlit as st

def process():		
		if not st.session_state.name.strip() or not st.session_state.password.strip():
			st.error("Please fill in both fields.")
		else:
			st.success(f"Hello, {st.session_state.name}!")
			st.info(f"Your password is: {st.session_state.password}")

with st.form("my_form", clear_on_submit=True):
	#st.write('counter')
	name = st.text_input("Enter your name", key="name")
	password = st.text_input("Enter your password", key="password", type="password")
	submitted = st.form_submit_button("Submit", on_click= process)
		#st.write(f"Hello, {name}!")
		#st.write(f"Your password is: {password}")
