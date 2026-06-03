from genericpath import exists
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import json
import os
import uuid
import base64

# =====================================================
# CONFIG
# =====================================================

CHAT_DIR = "chat_sessions"
os.makedirs(CHAT_DIR, exist_ok=True)

st.set_page_config(
    page_title="🐍 Pymentor",
    layout="centered"
)

# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

/* Prevent footer overlap */
.main {
    padding-bottom: 140px;
}

/* Fixed uploader */
div[data-testid="stFileUploader"] {
    position: fixed;
    bottom: 75px;
    right: 20px;
    width: 220px;
    z-index: 999;
    background: white;
    padding: 6px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

/* Cleaner sidebar buttons */
.stButton button {
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# OPENAI CLIENT
# =====================================================

@st.cache_resource
def load_api_client():
    load_dotenv()
    return OpenAI()

client = load_api_client()

# =====================================================
# SESSION STATE
# =====================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# =====================================================
# HELPERS
# =====================================================

def default_messages():
    return [
        {
            "role": "system",
            "content": "You are a helpful Python assistant."
        }
    ]


def save_chat_history(session_id, messages):
    filepath = os.path.join(CHAT_DIR, f"{session_id}.json")

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=4)
    except Exception as e:
        st.error(f"Error saving chat: {e}")


def load_chat_history(session_id):
    filepath = os.path.join(CHAT_DIR, f"{session_id}.json")

    if exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default_messages()

    return default_messages()


def delete_chat_history(session_id):
    filepath = os.path.join(CHAT_DIR, f"{session_id}.json")

    if exists(filepath):
        os.remove(filepath)


def get_chat_title(messages):
    for msg in messages:
        if msg.get("role") == "user":
            content = msg.get("content")

            if isinstance(content, str):
                return content[:30]

            elif isinstance(content, list):
                for item in content:
                    if item.get("type") == "input_text":
                        return item.get("text", "")[:30]

    return None


def encode_image(uploaded_file):
    uploaded_file.seek(0)
    return base64.b64encode(uploaded_file.read()).decode("utf-8")


# =====================================================
# AI RESPONSE
# =====================================================

def chat_with_ai(messages, placeholder, model):
    response = client.responses.create(
        model=model,
        input=messages,
        stream=True,
        store=False
    )

    final_text = ""

    for event in response:
        if event.type == "response.output_text.delta":
            final_text += event.delta
            placeholder.markdown(final_text)

    return final_text


# =====================================================
# HEADER
# =====================================================

st.title("🐍 Pymentor App")

# =====================================================
# MODEL SELECTOR
# =====================================================

model = st.sidebar.selectbox(
    "Select Model",
    [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4.1",
        "gpt-4.1-mini"
    ]
)

# =====================================================
# NEW CHAT
# =====================================================

if st.sidebar.button("➕ New Chat"):
    st.session_state.session_id = str(uuid.uuid4())
    st.session_state.messages = default_messages()
    st.rerun()

# =====================================================
# LOAD CURRENT CHAT
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history(
        st.session_state.session_id
    )

# =====================================================
# SIDEBAR METRICS
# =====================================================

message_count = len([
    m for m in st.session_state.messages
    if m["role"] != "system"
])

st.sidebar.metric("☁️ Messages", message_count)
st.sidebar.title("Recent Chats")

# =====================================================
# SIDEBAR CHATS
# =====================================================

session_files = os.listdir(CHAT_DIR)

for file in session_files:

    session_id = file.replace(".json", "")
    chat_messages = load_chat_history(session_id)

    has_user_message = any(
        msg.get("role") == "user"
        for msg in chat_messages
    )

    if not has_user_message:
        continue

    title = get_chat_title(chat_messages)

    if not title:
        continue

    col1, col2 = st.sidebar.columns([5, 1])

    with col1:
        if st.button(title, key=f"chat_{session_id}"):
            st.session_state.session_id = session_id
            st.session_state.messages = load_chat_history(session_id)
            st.rerun()

    with col2:
        if st.button("🗑️", key=f"delete_{session_id}"):
            delete_chat_history(session_id)
            st.rerun()

# =====================================================
# FILE UPLOADER
# =====================================================

uploaded_file = st.file_uploader(
    "",
    type=["png", "jpg", "jpeg"],
    label_visibility="collapsed"
)

if uploaded_file:
    st.session_state.uploaded_file = uploaded_file

# =====================================================
# FILE PREVIEW
# =====================================================

file = st.session_state.get("uploaded_file")

if file:
    col1, col2 = st.columns([5, 1])

    with col1:
        st.image(file.getvalue(), width=140)

    with col2:
        if st.button("❌ Remove"):
            st.session_state.uploaded_file = None
            st.rerun()

# =====================================================
# CHAT MESSAGES
# =====================================================

for msg in st.session_state.messages:

    if msg["role"] == "system":
        continue

    with st.chat_message(msg["role"]):

        content = msg["content"]

        if isinstance(content, str):
            st.write(content)

        elif isinstance(content, list):

            for item in content:

                if item["type"] == "input_text":
                    st.write(item["text"])

                elif item["type"] == "input_image":
                    st.image(item["image_url"], width=250)

# =====================================================
# CHAT INPUT
# =====================================================

message = st.chat_input("Ask me anything...")

# =====================================================
# SEND MESSAGE
# =====================================================

if message or st.session_state.uploaded_file:

    content = []

    if not message:
        message = "Explain this image"

    content.append({
        "type": "input_text",
        "text": message
    })

    # IMAGE
    if st.session_state.uploaded_file:

        base64_image = encode_image(
            st.session_state.uploaded_file
        )

        content.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{base64_image}"
        })

    user_message = {
        "role": "user",
        "content": content
    }

    st.session_state.messages.append(user_message)

    # USER UI
    with st.chat_message("user"):

        if message:
            st.markdown(message)

        if st.session_state.uploaded_file:
            st.image(
                st.session_state.uploaded_file.getvalue(),
                width=300
            )

    # ASSISTANT UI
    with st.chat_message("assistant"):

        placeholder = st.empty()

        ai_reply = chat_with_ai(
            st.session_state.messages,
            placeholder,
            model
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })

    save_chat_history(
        st.session_state.session_id,
        st.session_state.messages
    )

    st.session_state.uploaded_file = None

    st.rerun()
