
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
BASE = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
API_URL = f"{BASE}/api/chat"

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))

st.set_page_config(page_title="Companion AI", page_icon="💬")
st.title("Companion AI")
st.caption("A safe space to be heard.")

DEFAULTS = {"session": None, "messages": []}
for key, value in DEFAULTS.items():
    st.session_state.setdefault(key, value)

if st.session_state.session is None:
    tab_login, tab_signup = st.tabs(["Log in", "Sign up"])
    with tab_login:
        email = st.text_input("Email", key="li_email")
        pw = st.text_input("Password", type="password", key="li_pw")
        if st.button("Log in"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": pw})
                st.session_state.session = res.session
                st.rerun()
            except Exception:
                st.error("Incorrect email or password.")
    with tab_signup:
        email = st.text_input("Email", key="su_email")
        pw = st.text_input("Password", type="password", key="su_pw")
        if st.button("Create account"):
            try:
                supabase.auth.sign_up({"email": email, "password": pw})
                st.success("Account created. Check your email, then log in.")
            except Exception:
                st.error("Could not create account.")
    st.stop()

token = st.session_state.session.access_token

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
                response = requests.post(
                    API_URL, 
                    json={"message": user_input},
                    headers={"Authorization" : f"Bearer {token}"},
                    timeout=60)
                if response.status_code in (401,403):
                    st.session_state.session = None
                    st.rerun()
                response.raise_for_status()
                reply = response.json()["reply"]
            except Exception:
                reply = "Sorry, something went wrong. Please try again."

        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
