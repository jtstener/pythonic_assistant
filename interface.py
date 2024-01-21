"""
File: interface.py
Author: Julius Stener (really the streamlit team for most of it)
Reason: 
"""

import streamlit as st
import time
import random
from pythonic_assistant.pythonic_assistant import PythonicAssistant

st.title("Assistant")

# Initialize the PythonicAssistant
if "assistant" not in st.session_state:
    
    name = "US Department of Defense Acquisitions Expert"
    description = "You are an expert in DoD Acquistions. Draw on your existing knowledge of the National Defense Authorization Act (NDAA) and Pentagon's Budget Materials."
    instructions = "Please address the user as Jane Doe. The user has a premium account."

    st.session_state.assistant = PythonicAssistant(
        name = name,
        description = description,
        instructions = instructions
    )

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("How can I help you today?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    assistant_response = st.session_state.assistant.execute(
        st.session_state.messages, 
        as_list=True
        )
    response = assistant_response[-1]['content']

    with st.chat_message("assistant"):
        st.markdown(response)
    
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})