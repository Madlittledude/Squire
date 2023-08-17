import boto3
import json
import os
import tempfile
from datetime import datetime
import streamlit as st

class ChatLogger:
    def __init__(self, username):
        self.username = username
        self.access = os.environ['ACCESS_KEY']
        self.secret = os.environ['SECRET_KEY']
        self.date = datetime.utcnow().strftime('%Y-%m-%d')
        self.load_existing_logs()
        self.start_new_session()

    def load_existing_logs(self):
        key = f'{self.username}_chat_history.json'
        try:
            s3 = boto3.client('s3', aws_access_key_id=self.access, aws_secret_access_key=self.secret)
            response = s3.get_object(Bucket="brainstormdata", Key=key)
            self.chat_history = json.loads(response['Body'].read().decode('utf-8'))
        except:
            self.chat_history = {"user_id": self.username, "logs": []}


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

    
    import tempfile
    access = os.environ['ACCESS_KEY']
    secret = os.environ['SECRET_KEY']
    def upload_to_aws(self, local_file, bucket, s3_file):
        s3 = boto3.client('s3',access,secret)

        try:
            s3.upload_file(local_file, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except Exception as e:
            print("Something went wrong:", e)
            return False

    def save_chat_to_json(self):
        key = f'{self.username}_chat_history.json'
        chat_json = json.dumps(self.chat_history)

        # Create a temporary file to hold the JSON data
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
            temp_file.write(chat_json)
            temp_file_path = temp_file.name

        # Define your S3 bucket name and file path
        bucket = 'brainstormdata'
        s3_file_path = f"{bucket}/{key}"

        # Upload the temporary file to S3 using the upload_to_aws function
        success = self.upload_to_aws(temp_file_path, bucket, s3_file_path)

        if success:
            print("Upload successful")
            os.remove(temp_file_path)  # Remove the temporary file
        else:
            print("Failed to upload file to S3")
