import streamlit as st
st.title('💬 Chat Session with Persistent State')
if "messages" not in st.session_state:
  st.session_state.messages = []

#if st.session_state.messages:
for message in st.session_state.messages:
          with st.chat_message(message['role']):
             st.write(message['content'])    
user_input= st.chat_input('Type your message here...')
  
if user_input:
 # st.write(f'You: {user_input}')
  st.session_state.messages.append({'role': 'user', 'content': user_input})
  st.session_state.messages.append({'role': 'assistant', 'content': f'Agent: {user_input}'})

