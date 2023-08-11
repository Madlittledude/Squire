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
        self.chat_logs = {
            "username": username,
            "chat_logs": []
        }

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
        # Log the chat messages
        chat_entry = {"user": user_message, "assistant": assistant_message}
        if not self.chat_logs["chat_logs"]:
            self.chat_logs["chat_logs"].append({
                "day": datetime.now().strftime("%Y-%m-%d"),
                "sessions": [{"session_start_time": datetime.now().strftime("%I:%M %p"), "chat": [chat_entry]}]
            })
        else:
            current_day_log = self.chat_logs["chat_logs"][-1]
            if current_day_log["day"] == datetime.now().strftime("%Y-%m-%d"):
                current_day_log["sessions"][-1]["chat"].append(chat_entry)
            else:
                self.chat_logs["chat_logs"].append({
                    "day": datetime.now().strftime("%Y-%m-%d"),
                    "sessions": [{"session_start_time": datetime.now().strftime("%I:%M %p"), "chat": [chat_entry]}]
                })

    def save_chat_to_json(self):
        # Save the chat logs to a JSON file
        filename = 'test1.json'
        with open(filename, 'w') as file:
            json.dump(self.chat_logs, file)

        # Upload the JSON file to S3
        client = boto3.client('s3', aws_access_key_id="ACCESS_KEY", aws_secret_access_key="SECRET_KEY")
        upload_file_bucket = 'brainstormdata'
        upload_file_key = str('test1.json')
        client.upload_file(filename, upload_file_bucket, upload_file_key)
        
def display_chat_message(role, content, avatar):
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)


user = "https://raw.githubusercontent.com/Madlittledude/Squire/main/Assets/madlittledude_flipped.png"
assistant = "https://raw.githubusercontent.com/Madlittledude/Squire/main/Assets/Madlittledude_2.png"
