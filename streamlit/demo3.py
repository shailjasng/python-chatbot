import streamlit as st
if 'count' not in st.session_state:
				st.session_state.count = 0
def counter():

		st.session_state.count += 1
		st.write('Count:', st.session_state.count)
		#st.write('Count:, lambda: ', st.session_state.count+=1)


st.button('Click me', on_click=counter)

