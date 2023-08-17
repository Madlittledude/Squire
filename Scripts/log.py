import boto3
import json
from datetime import datetime
import os

class ChatLogger:
    def __init__(self, username):
        self.username = username
        self.date = datetime.utcnow().strftime('%Y-%m-%d')
        self.client = boto3.client('s3',
                           region_name='us-west-1',
                           aws_access_key_id=os.environ["ACCESS_KEY"],
                           aws_secret_access_key=os.environ["SECRET_KEY"])
        self.load_existing_logs()
        self.start_new_session()



    def load_existing_logs(self):
        bucket_name = 'brainstormdata'
        key = f'{self.username}_chat_history.json'
        try:
            response = self.client.get_object(Bucket=bucket_name, Key=key)
            self.chat_history = json.load(response['Body'])
        except:
            self.chat_history = {"user_id": self.username, "logs": []}
        today_log = [log for log in self.chat_history["logs"] if log["date"] == self.date]
        self.session_count = len(today_log[0]["sessions"]) if today_log else 0

    def start_new_session(self):
        session_data = {
            "session_id": f"session{self.session_count + 1}",
            "messages": []
        }
        today_log = [log for log in self.chat_history["logs"] if log["date"] == self.date]
        if today_log:
            today_log[0]["sessions"].append(session_data)
        else:
            date_log = {
                "date": self.date,
                "sessions": [session_data]
            }
            self.chat_history["logs"].append(date_log)
        self.session_count += 1

    
    def log_chat(self, user_message, assistant_message):
        time_now = datetime.utcnow().strftime('%H:%M:%S')
        if user_message:
            self.chat_history["logs"][-1]["sessions"][-1]["messages"].append(
                {"sender": "user", "message": user_message, "time": time_now}
            )
        if assistant_message:
            self.chat_history["logs"][-1]["sessions"][-1]["messages"].append(
                {"sender": "assistant", "message": assistant_message, "time": time_now}
            )


    def save_chat_to_json(self, messages, openai_model):
        session_messages = []
        for message in messages:
            if message["role"] == "user":
                sender = "user"
                content = message["content"]
            else:
                sender = "assistant"
                response = openai_model.send_message(message["content"])  # Replace with actual OpenAI interaction
                content = response["choices"][0]["message"]["content"]
            time_now = datetime.utcnow().strftime('%H:%M:%S')
            session_messages.append({"sender": sender, "message": content, "time": time_now})
        
        if self.chat_history["logs"]:
            self.chat_history["logs"][-1]["sessions"][-1]["messages"] = session_messages
        else:
            self.chat_history["logs"].append({"date": self.date, "sessions": [{"session_id": "session1", "messages": session_messages}]})

        self.save_chat_to_json()  # Corrected method name

