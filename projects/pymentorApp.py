from genericpath import exists
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import time 
import json
import os
import uuid
import base64

#client = OpenAI()
CHAT_DIR = "chat_sessions"

os.makedirs(CHAT_DIR, exist_ok=True)

# -------------------------------
# OPEN AI CONNECTION
# -------------------------------
def load_api_client():
    load_dotenv()
    return OpenAI()

client = load_api_client();

# -------------------------------
# Sessions 
# -------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# if "show_uploader" not in st.session_state:
#     st.session_state.show_uploader = False

# -------------------------------
# Helpers
# -------------------------------

def save_chat_history(session_id, messages):
   filepath = os.path.join(CHAT_DIR, f"{session_id}.json")
   with open(filepath, "w") as f:
      json.dump(messages, f, indent=4)

def load_chat_history(session_id):
   filepath = os.path.join(CHAT_DIR, f"{session_id}.json")
   if exists(filepath):
      with open(filepath, "r") as f:
        return json.load(f)
   else:
      messages = [
         {"role": "system",
          "content": "You are a helpful assistant"
           #"You are a strict Python assistant.\n"
           # "You ONLY answer questions related to Python programming.\n"
           # "If a question is not related to Python, you MUST respond exactly with:\n"
            #"'Sorry, I only answer Python-related questions.'\n"
            #"Do not provide any additional explanation."
         }]
      return messages

def del_chat_history(session_id):
     filepath = os.path.join(CHAT_DIR, f"{session_id}.json")
     if exists(filepath):
         os.remove(filepath)  
        #reset the deleted chat in the page
         st.session_state.session_id = str(uuid.uuid4())
         st.session_state.messages = [
         {
            "role": "system",
            "content": "You are a Python assistant"
         }]
      
def chat_with_ai(messages,placeholder,model):
    response = client.responses.create(
        model=model,
        input=messages,
        store=False, 
        stream=True
    )
    # in case of streaming response, we need to concatenate the chunks to get the final response text
    final_text = ''
    #placeholder = st.empty()
    for event in response:
         # print(event.type)
          if event.type == "response.output_text.delta":
            #print(event.delta, end="")
            final_text += event.delta
            placeholder.markdown(final_text)
            time.sleep(0.02)
    
    return final_text

st.set_page_config('🐍 pymentor', layout='centered')
st.title('🐍 Pymentor App')

model = st.sidebar.selectbox("Select Model",['gpt-4o','gpt-4o-mini', 'gpt-4.1', 'gpt-4.1-mini'])
if st.sidebar.button("New Chat"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are python assistant."
        }
    ]

    st.rerun()
if "messages" not in st.session_state:
   st.session_state.messages = load_chat_history(st.session_state.session_id)

def get_chat_title(messages): 
   content = ''
   for msg in messages:
      if msg['role'] == 'user':
        content =  msg['content']
        if isinstance(content, str):
          return content[:30]
        elif isinstance(content, list):
           for item in content:
              if item['type'] == 'input_text':
                return item['text'][:30]
   return 'New Chat'

def encode_image(uploaded_file):
     uploaded_file.seek(0)
     return  base64.b64encode(uploaded_file.read()).decode("utf-8")

message_count =len([m for m in st.session_state.messages if m['role']!= 'system'])
count = st.sidebar.metric("☁️Messages:", message_count)
st.sidebar.title('Recent Chats')
session_files = os.listdir(CHAT_DIR)
for file in session_files:
   session_id = file.replace('.json', '')
   chat_messages = load_chat_history(session_id)
   #skip system only chats
   # for msg in chat_messages:
   #   if msg["role"] != "user":
   #      continue
   has_user_message = any(
      msg.get('role') == 'user'
      for msg in chat_messages
   )
   if not has_user_message:
      continue
   title = get_chat_title(chat_messages)
   #  if st.sidebar.button(title[:30], key=f"chat_{session_id}_{i}"):
   title = title or 'New Chat'
   col1, col2 = st.sidebar.columns([5,1])
   with col1:
     if st.button(title, key=session_id):
      st.session_state.session_id = session_id
      st.session_state.messages = load_chat_history(session_id)     
      st.rerun()
   
   with col2:
      if st.button("🗑️", key=f"delete_{session_id}"):
        del_chat_history(session_id)
        st.rerun()

chat_container = st.container()

# -------------------------------
# File Preview (Copilot style)
# -------------------------------
# file = st.session_state.get("uploaded_file")

# if file:
#     col1, col2 = st.columns([5, 1])

#     with col1:
#         st.image(file, width=120)

#     with col2:
#         if st.button("❌", key="remove_file"):
#             st.session_state.uploaded_file = None
#             st.rerun()

with chat_container:
  if st.session_state.messages:
     for msg in st.session_state.messages:
       if (msg['role'] != 'system'):
         with st.chat_message(msg['role']):
           content = msg['content']
           if isinstance(content, str):
             st.write(content);
           elif isinstance(content, list):
              for item in content:
                if item['type']== "input_text":
                  st.write(item["text"])
                elif item['type']== "input_image":
                  st.image(item["image_url"], width=250)

# with st.form ('pymentor_form', clear_on_submit= True):
#   message = st.text_area('Where should we begin?',
#                           height=100,
#                           placeholder="Ask Anything about Python")
#   submit = st.form_submit_button('Submit')

# -------------------------------
# Attach Button
# -------------------------------
# col1, col2 = st.columns([1, 8])

# with col1:
#     if st.button("📎", key="attach_btn"):
#         st.session_state.show_uploader = True

if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0

uploaded_file = st.file_uploader(
    "",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed",
    key=f"uploader_{st.session_state.uploader_key}"
)

if uploaded_file:
    st.session_state.uploaded_file = uploaded_file
message = st.chat_input("Ask me anything...")
if message:
   content = []
   # if not message:
   #   message = "Explain this image"

   content.append({
            "type": "input_text",
            "text":message
      })
   if st.session_state.uploaded_file:
      st.session_state.uploaded_file.seek(0)
      base64_image = encode_image(st.session_state.uploaded_file)
      content.append({
         "type": "input_image",
         "image_url": f"data:image/jpeg;base64,{base64_image}"
      })

   user_message = {
         "role": "user",
         "content": content
      }       
   st.session_state.messages.append(user_message)

   with st.chat_message("user"):
         if message:
           st.markdown(message)
         if st.session_state.uploaded_file:
            st.session_state.uploaded_file.seek(0)
            st.image(st.session_state.uploaded_file, width= 300)
   with st.chat_message("assistant"):
              placeholder = st.empty()
              typing = st.empty()
              typing.markdown("🕟Your pymentor tutor is typing........");
              ai_reply = chat_with_ai(st.session_state.messages,placeholder,model)
              typing.write('')
              st.session_state.messages.append({
               "role": "assistant",
               "content": ai_reply
            })
   save_chat_history(st.session_state.session_id, st.session_state.messages)
   st.session_state.uploaded_file = None
   # Reset uploader widget
   st.session_state.uploader_key += 1
   st.rerun()

# -------------------------------
# Show uploader only when needed
# -------------------------------
# if st.session_state.show_uploader:
#     uploaded_file = st.file_uploader(
#         "",
#         type=["png", "jpg", "jpeg"],
#         label_visibility="collapsed"
#     )

#     if uploaded_file:
#         st.session_state.uploaded_file = uploaded_file
#         st.session_state.show_uploader = False
#         st.rerun()
  



