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
        if not self.chat_logs["chat_logs"]:
            print("No chat logs to save.")  # Or handle this situation in a way that makes sense for your application
            return
    
        current_chat_session = {
            "username": self.username,
            "time": datetime.now().strftime("%I:%M %p"),
            "chat": self.chat_logs["chat_logs"][-1]  # Now safe to access because we know there's at least one element
        }
    
        filename = f'{self.username}_{datetime.now().strftime("%Y%m%d%H%M%S")}.json'
        with open(filename, 'w') as file:
            json.dump(current_chat_session, file)
    
        aws_access_key_id = os.environ['ACCESS_KEY']
        aws_secret_access_key = os.environ['SECRET_KEY']
    
        client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        upload_file_bucket = 'brainstormdata'
        upload_file_key = filename
        client.upload_file(filename, upload_file_bucket, upload_file_key)



