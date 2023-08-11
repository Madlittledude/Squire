import streamlit as st
import openai
import json
import boto3
from datetime import datetime
from log import ChatLogger


class ChatManager:
    def __init__(self, session_state, openai_model, username):
        self.session_state = session_state
        self.openai_model = openai_model
        self.username = username
        self.logger = ChatLogger(username)
   

    def display_chat_message(self, role, content, avatar):
        with st.chat_message(role, avatar=avatar):
            st.markdown(content)

    def display_chat_interface(self):
        for message in self.session_state.messages:
            if message["role"] == "system":
                continue
            avatar = assistant if message["role"] == "assistant" else user
            self.display_chat_message(message["role"], message["content"], avatar)

        prompt = st.chat_input("What are ya working on : )")
        if prompt:
            self.session_state.first_message_sent = True
            self.session_state.messages.append({"role": "user", "content": prompt})
            self.display_chat_message("user", prompt, user)

            with st.chat_message("assistant", avatar=assistant):
                message_placeholder = st.empty()
                full_response = ""
                for response in openai.ChatCompletion.create(
                    model=self.openai_model,
                    messages=([
                        {"role": m["role"], "content": m["content"]}
                        for m in self.session_state.messages
                    ]),
                    stream=True,
                ):
                    full_response += response.choices[0].delta.get("content", "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
                self.session_state.messages.append({"role": "assistant", "content": full_response})
                self.log_chat(prompt, full_response)


    def log_chat(self, user_message, assistant_message):
        self.logger.log_chat(user_message, assistant_message) 


    def save_chat_to_json(self):
        self.logger.save_chat_to_json()  # Call the save_chat_to_json method of ChatLogger


        
def display_chat_message(role, content, avatar):
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)


user = "https://raw.githubusercontent.com/Madlittledude/Squire/main/Assets/madlittledude_flipped.png"
assistant = "https://raw.githubusercontent.com/Madlittledude/Squire/main/Assets/Madlittledude 2.png"
