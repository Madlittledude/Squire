import json
import boto3
from datetime import datetime

class ChatLogger:
    def __init__(self, username):
        self.username = username
        self.chat_logs = {
            "username": username,
            "chat_logs": []
        }

    def log_chat(self, user_message, assistant_message):
        chat_entry = {"user": user_message, "assistant": assistant_message}
        current_day = datetime.now().strftime("%Y-%m-%d")
        if not self.chat_logs["chat_logs"] or self.chat_logs["chat_logs"][-1]["day"] != current_day:
            self.chat_logs["chat_logs"].append({
                "day": current_day,
                "sessions": [{"session_start_time": datetime.now().strftime("%I:%M %p"), "chat": []}]
            })
        
        self.chat_logs["chat_logs"][-1]["sessions"][-1]["chat"].append(chat_entry)
        self.save_chat_to_json() # Save the chat log immediately after logging

    def save_chat_to_json(self):
        filename = f'{self.username}_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
        with open(filename, 'w') as file:
            json.dump(self.chat_logs, file)

        aws_access_key_id = os.environ['ACCESS_KEY']
        aws_secret_access_key = os.environ['SECRET_KEY']

        client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        upload_file_bucket = 'brainstormdata'
        upload_file_key = filename
        client.upload_file(filename, upload_file_bucket, upload_file_key)

