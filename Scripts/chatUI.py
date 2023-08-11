import streamlit as st
import openai
import json
import boto3
from datetime import datetime

class ChatManager:
    def __init__(self, session_state, openai_model, username):
        self.session_state = session_state
        self.openai_model = openai_model
        self.username = username
        self.current_chat = []

    def display_chat_interface(self):
        for message in self.session_state.messages:
            if message["role"] == "system":
                continue
            avatar = assistant if message["role"] == "assistant" else user
            display_chat_message(message["role"], message["content"], avatar)

        prompt = st.chat_input("What are ya working on : )")
        if prompt:
            self.handle_user_input(prompt)

    def handle_user_input(self, prompt):
        self.session_state.messages.append({"role": "user", "content": prompt})
        response = openai.ChatCompletion.create(
            model=self.openai_model,
            messages=([
                {"role": m["role"], "content": m["content"]}
                for m in self.session_state.messages
            ])
        )
        assistant_response = response['choices'][0]['message']['content']
        self.session_state.messages.append({"role": "assistant", "content": assistant_response})
        self.current_chat.append({"user": prompt, "assistant": assistant_response})

    def save_chat_to_json(self):
        chat_logs = {
            "username": self.username,
            "chat_logs": [
                {
                    "day": datetime.now().strftime("%Y-%m-%d"),
                    "sessions": [
                        {
                            "session_start_time": datetime.now().strftime("%I:%M %p"),
                            "chat": self.current_chat
                        }
                    ]
                }
            ]
        }
        with open('test1.json', 'w') as file:
            json.dump(chat_logs, file)

        client = boto3.client('s3', aws_access_key_id="ACCESS_KEY", aws_secret_access_key="SECRET_KEY")
        upload_file_bucket = 'brainstormdata'
        upload_file_key = str('test1.json')
        client.upload_file('test1.json', upload_file_bucket, upload_file_key)

def display_chat_message(role, content, avatar):
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

user = "https://raw.githubusercontent.com/Madlittledude/Squire/main/Assets/madlittledude_flipped.png"
assistant = "https://raw.githubusercontent.com/Madlittledude/Squire/main/Assets/madlittledudette_flipped.png"
