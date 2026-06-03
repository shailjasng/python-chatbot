import streamlit as st
from datetime import datetime
import time

st.write("Clock")
placeholder = st.empty()
#while True:
for _ in range(60):
  now =datetime.now()
  placeholder.write(now.strftime('%H:%M:%S'))
  time.sleep(1)
  
