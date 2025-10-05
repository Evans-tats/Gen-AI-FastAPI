import requests
import streamlit as st

st.title("💬 basic web scrapper")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("wriite your prompt in here"):
    st.session_state.messages.append({"role": "user", "content" : prompt})

    with st.chat_message("user"):
        st.text(prompt)
    payload = {
        "prompt": prompt,
        "model": "gemini-1.5-flash" 
    }
    response = requests.post(
        f"http://127.0.0.1:8000/generate/text", json=payload
    )
    response.raise_for_status()
    with st.chat_message("ai"):
        st.markdown(response.text)