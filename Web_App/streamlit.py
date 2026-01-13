import streamlit as st

st.title('YouTube Video Downloader')
URL = st.text_input('Enter the link',args="Paste your link here!")
st.button('Start Download') 

st.video(URL)