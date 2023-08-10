
import os

def load_credentials():
    # Load the TOML content from an environment variable
    credentials = os.environ['CREDENTIALS']
  
    return credentials

def authenticate(username, password):
    credentials = load_credentials()
    # Check if the provided username and password match the stored credentials
    if username in credentials['users'] and credentials['users'][username] == password:
        return True
    return False
