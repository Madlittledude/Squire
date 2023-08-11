import streamlit as st
import openai
import os
from chatUI import ChatManager  # Import the ChatManager class
from auth import load_credentials, authenticate

# Set up the page layout
st.set_page_config(page_title="Squire_chat", page_icon="./Assets/pixel_pencil.png", layout='centered')

def display_login():
    st.title("Login to Brain Storm :lightning:")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.username = username
            st.session_state.logged_in = True
            st.success("Login successful!")
        else:
            st.error("Invalid username or password.")

def display_intro():
    st.title("Welcome to Your Session with Brain Storm :lightning:")
    st.write("Here's how it can assist you:")
    st.write("- **Drafting Emails:** Just tell it what you want in your email and in what tone you'd like it said.")
    st.write("- **Summarizing Text:** It can help you craft concise summaries, giving you a starting point for understanding complex documents. Simply copy and paste the text into the chatbox.")
    st.write("- **Creating outlines:** Create outlines with just a few ideas in your prompt. The more detailed you are, the better the response.")
    st.write("- **Brainstorming and Organizing Thoughts:** It will help you layout, shape, and explore ideas.")
    st.write("- **Structuring Unstructured Text:** It guides you in organizing chaotic text.")
    st.write("- **Extracting Information:** It can help you extract information from text, such as names, dates, and other relevant information you can articulate.")
    st.write("Brain Storm can help you form the question you need to solve your problem.")
    st.write("Remember, it is not a factbook; think of this tool as a springboard for your ideas and a way to initiate work product. However, since it only knows about many topics pre-September 2021, those facts will be most reliable.")
    st.write(":heart: Max")

# Initialization logic
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "system",
        "content": ("You are Brain Storm the virtual train of thought assistant working at a municipal law firm."
                    "You are a comforting,nurturing robot, so it will help to gain an understanding of the user's writing and work style. 
                    Ask them what they're working on and figure out how you as Generative Ai can be most useful."
                    "Your primary role is to facilitate productive and constructive "
                    "brainstorm sessions. The user may copy and paste text from other sources or input their "
                    "own text, and you'll assist in structuring their thoughts."
                    "Your professional specialties as an assistant include:\n"
                    "- Summarizing text\n"
                    "- Creating outlines for anything you're working on. Just have them give you some points to follow\n"
                    "- Understanding and articulating the construction of ideas in text\n"
                    "- Brainstorming and organizing thoughts\n"
                    "- Structuring unstructured text\n"
                    "- Extracting information from text\n"
                    )
    }]

if "first_message_sent" not in st.session_state:
    st.session_state.first_message_sent = False

openai.api_key = os.environ["OPENAI_API_KEY"]

# Display logic
if st.session_state.logged_in:
    if not st.session_state.first_message_sent:
        display_intro()
    chat_manager = ChatManager(st.session_state, st.session_state["openai_model"], st.session_state.username)  # Create an instance of ChatManager
    chat_manager.display_chat_interface()  # Call the display_chat_interface method
else:
    display_login()

# Save chat to JSON and upload to S3 when the session ends
if st.button("End Session"):
    chat_manager.save_chat_to_json()
    st.success("Session ended and chat logs saved.")



