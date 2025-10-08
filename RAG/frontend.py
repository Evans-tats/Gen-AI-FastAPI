import streamlit as st
import requests

st.write("upload a file to FastAPI")
file = st.file_uploader("choose file", type=pdf)
if st.button("Submit"):
    if file is not None:
        file = {"file" : (file.name, file,file.type)}
        response = requests.post("http://localhost:8000/upload", files=file)
        st.write(response.text)
    else:
        st.write("no file uploaded")