import streamlit as st
import sys
from openai import OpenAI
import os
from dotenv import load_dotenv
import client
import requests

sys.path.append(".")

load_dotenv()

def on_btn_click():
    del st.session_state.messages

def getresponse(prompt: str):
    
    response = requests.post(url=client.SERVER_URL + "/", 
                             json={"question": prompt},
                             stream=True)
    return response.json()["text"]["output"]
    # response.json()["text"] # for Classical RAG

def uploadfile():
    uploaded_file = st.file_uploader("Bạn muốn hiểu tài liệu tốt hơn, hãy đẩy vào đây nha 😊")

    if uploaded_file is not None:
        # bytes_data = uploaded_file.read()
        # text_data = str(bytes_data, 'utf-8')  # Decode bytes to text (assuming text file)
        response = requests.post(client.SERVER_URL_API + "/add_data",
                                files={"files": uploaded_file})
        # print(response.json()["status"])
        st.warning(response.json()["status"])

def main():

    USER_AVATAR = "👤"
    BOT_AVATAR = "🤖"

    st.set_page_config(
        page_title="SunSun - hệ thống hỏi đáp",
        page_icon="💬",
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None,
    )

    uploadfile()
        
    st.header("SunSun☀️💁")

    if client.get_fastapi_status() is False:
        st.warning("FastAPI is not ready. Make sure your backend is running")
        st.stop()  # exit application after displaying warning if FastAPI is not available

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("How can I help ?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container

        with st.chat_message("user", avatar=USER_AVATAR):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar=BOT_AVATAR):
            message_placeholder = st.empty()
            full_response = ""
            full_response += getresponse(prompt)
            message_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    st.button('Clear Message', on_click=on_btn_click)

    st.markdown(
        """
        I am building and maintaining the SunSun project and I am excited to share this project with you!

    ⭐️ me on [GitHub](https://github.com/ngoctuannguyen/SunSunChatBot)

    📝 leave me an [issue](https://github.com/ngoctuannguyen/SunSunChatBot/issues) if you find something
    """
    )

if __name__ == '__main__':
   main()
