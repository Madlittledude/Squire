class ChatLogger:
    def __init__(self, username):
        self.username = username
        self.date = datetime.utcnow().strftime('%Y-%m-%d')
        self.client = boto3.client('s3',
                                   region_name='us-west-1',
                                   aws_access_key_id=os.environ["ACCESS_KEY"],
                                   aws_secret_access_key=os.environ["SECRET_KEY"])
        self.load_existing_logs()

    def load_existing_logs(self):
        bucket_name = 'brainstormdata'
        key = f'{self.username}_chat_history.json'
        try:
            response = self.client.get_object(Bucket=bucket_name, Key=key)
            self.chat_history = json.load(response['Body'])
        except:
            self.chat_history = {"user_id": self.username, "logs": []}
        today_log = [log for log in self.chat_history["logs"] if log["date"] == self.date]
        if not today_log:
            self.chat_history["logs"].append({"date": self.date, "messages": []})

    def log_chat(self, user_message, assistant_message):
        time_now = datetime.utcnow().strftime('%H:%M:%S')
        today_log = [log for log in self.chat_history["logs"] if log["date"] == self.date][0]
        if user_message:
            today_log["messages"].append({"sender": "user", "message": user_message, "time": time_now})
        if assistant_message:
            today_log["messages"].append({"sender": "assistant", "message": assistant_message, "time": time_now})

    def save_chat_to_s3(self):
        # Save the chat history to S3 bucket
        bucket_name = 'brainstormdata'
        key = f'{self.username}_chat_history.json'
        self.client.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(self.chat_history, indent=2)
        )


