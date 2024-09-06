import streamlit as st
import openai
import os
from dotenv import load_dotenv


load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")

custom_prompt = "You are an empathetic assistant. You have to talk with empathy to user understanding his feelings and emotions. You have to be like a caring friend of the user replying every message like taking care of user's feelings."

def get_openai_response(user_input):
    try:
        
        completion = openai.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:personal::A4ObyrPQ",
            messages=[
                {"role": "system", "content": custom_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit app layout
st.title("model B - Finetuned Chatbot")

# the below snippet is for Initializing the  session state for storing the chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Text input field for the user to type a message
user_input = st.text_input("Type your message:", key="user_input")


if st.button("Send"):
    if user_input:
        # Adding user's message to session state
        st.session_state["messages"].append({"role": "user", "content": user_input})

        
        response = get_openai_response(user_input)

        # Adding GPT-4's response to session state
        st.session_state["messages"].append({"role": "assistant", "content": response})

# Display chat history
if st.session_state["messages"]:
    for message in st.session_state["messages"]:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**Bot:** {message['content']}")

# reset button to clear chat
if st.button("Clear Chat"):
    st.session_state["messages"] = []
