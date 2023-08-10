import streamlit as st

user = "https://raw.githubusercontent.com/Madlittledude/Squire/main/Assets/madlittledude_flipped.png"
assistant = "https://raw.githubusercontent.com/Madlittledude/Squire/main/Assets/madlittledudette_flipped.png"

def display_chat_message(role, content, avatar):
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

def display_chat_interface(session_state, openai, openai_model):
    for message in session_state.messages:
        if message["role"] == "system":
            continue
        avatar = assistant if message["role"] == "assistant" else user
        display_chat_message(message["role"], message["content"], avatar)

    prompt = st.chat_input("Start thinking with your fingers...get your thoughts out")
    if prompt:
        session_state.first_message_sent = True
        session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt, user)

        with st.chat_message("assistant", avatar=assistant):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=openai_model,
                messages=([
                    {"role": m["role"], "content": m["content"]}
                    for m in session_state.messages
                ]),
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        session_state.messages.append({"role": "assistant", "content": full_response})
