import json
import os
import streamlit as st
from st_files_connection import FilesConnection
from datetime import datetime

class ChatLogger:
    def __init__(self, username):
        self.username = username
        self.date = datetime.utcnow().strftime('%Y-%m-%d')
        self.conn = st.experimental_connection('s3', type=FilesConnection)  # Create connection object
        self.load_existing_logs()
        self.start_new_session()

    def load_existing_logs(self):
        key = f'{self.username}_chat_history.json'
        try:
            response = self.conn.read(f"brainstormdata/{key}", input_format="json", ttl=600)  # Adjusted read method
            self.chat_history = response
        except:
            self.chat_history = {"user_id": self.username, "logs": []}

        today_log = [log for log in self.chat_history["logs"] if log["date"] == self.date]
        self.session_count = len(today_log[0]["sessions"]) if today_log else 0

    def start_new_session(self):
        session_data = {"session_id": f"session{self.session_count + 1}", "messages": []}
        today_log = [log for log in self.chat_history["logs"] if log["date"] == self.date]
        if today_log:
            today_log[0]["sessions"].append(session_data)
        else:
            date_log = {"date": self.date, "sessions": [session_data]}
            self.chat_history["logs"].append(date_log)

        self.session_count += 1

    def log_chat(self, user_message, assistant_message):
        time_now = datetime.utcnow().strftime('%H:%M:%S')
        self.chat_history["logs"][-1]["sessions"][-1]["messages"].append(
            {"sender": "user", "message": user_message, "time": time_now}
        )
        self.chat_history["logs"][-1]["sessions"][-1]["messages"].append(
            {"sender": "assistant", "message": assistant_message, "time": time_now}
        )
        self.save_chat_to_json()

    def save_chat_to_json(self):
        key = f'{self.username}_chat_history.json'
        chat_json = json.dumps(self.chat_history)
        self.conn.write(f"brainstormdata/{key}", chat_json, overwrite=True)  # Adjusted write method
