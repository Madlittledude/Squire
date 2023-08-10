
import streamlit as st

def load_credentials():
    # Load the credentials from Streamlit's secrets
    credentials = st.secrets['users']
    return credentials

def authenticate(username, password):
    credentials = load_credentials()
    # Check if the provided username and password match the stored credentials
    if username in credentials and credentials[username] == password:
        return True
    return False
