"""
File: interface.py
Author: Julius Stener (really the streamlit team for most of it)
Reason: 
"""

# imports
import streamlit as st
import time
import random
from langserve import RemoteRunnable
from langchain_core.messages import HumanMessage, AIMessage

st.title("Assistant")

# Initialize the PythonicAssistant
if "assistant" not in st.session_state:
    
    name = "General Assistant"
    description = "You are a general assistant. Use the functions provided to follow the directions of the user."
    instructions = "Please address the user as Jane Doe. The user has a premium account."

    st.session_state.remote_runnable = RemoteRunnable("http://localhost:8000/")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add user message to messages
    st.session_state.messages.append({"role": "user", "content": prompt})

    ai_response = st.session_state.remote_runnable.invoke({"input": prompt, "chat_history": st.session_state.chat_history})

    st.session_state.chat_history.extend([HumanMessage(content=prompt), AIMessage(content=ai_response['output'])])

    with st.chat_message("assistant"):
        st.markdown(ai_response['output'])
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": ai_response['output']})