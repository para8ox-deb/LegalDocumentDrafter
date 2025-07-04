import streamlit as st
import os
from dotenv import load_dotenv
from modules.module1_drafting import module1_ui

# Loading the API key from .env file
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

st.set_page_config(page_title="Legal AI Suite", layout="wide")
st.title("Conversational Agentic AI Suite for Legal Document Drafting")

# Checking the API Key
if not api_key:
    st.error("OpenRouter API Key not found. Please add it to your .env file.")
    st.stop()

# Clear chat button
if st.button("Clear Drafting Chat", key="clear_drafting"):
    # Clear relevant session state keys
    st.session_state.pop("drafting_history", None)
    st.session_state.pop("drafting_chain", None)
    st.rerun()

# Displaying the UI for the drafting module
module1_ui(api_key)
