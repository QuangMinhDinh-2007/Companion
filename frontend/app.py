
import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
BASE = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
API_URL = f"{BASE}/api/chat"

st.set_page_config(page_title="Companion AI", page_icon="💬")
st.title("Companion AI")
st.caption("A safe space to be heard.")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = "test-user-001"  # replace with real auth later

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("What's on your mind?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner(""):
            try:
                response = requests.post(API_URL, json={
                    "user_id": st.session_state.user_id,
                    "message": user_input
                }, timeout=60)
                reply = response.json()["reply"]
            except Exception as e:
                reply = "Sorry, something went wrong. Please try again."
                st.exception(e)

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
