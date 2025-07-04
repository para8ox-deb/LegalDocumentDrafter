import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI

def setup_drafting_agent(api_key):
    #Setting up the conversational drafting agent to use a Deepseek V3 model from OpenRouter.

    llm = ChatOpenAI(
        model="deepseek/deepseek-chat-v3-0324:free",
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "http://localhost:8501", 
            "X-Title": "Legal AI Suite",
        },
        temperature=0.7,
        max_tokens=1024,
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a conversational AI assistant specializing in legal document drafting. Your goal is to help a user draft a legal document.

Instructions:
1. Start by asking the user what type of legal document they want to draft.
2. Identify key information needed and ask for it conversationally.
3. Use the conversation history to remember answers.
4. When you have gathered enough information, generate a complete, well-structured document.
"""
            ),
            MessagesPlaceholder(variable_name="history"), 
            ("human", "{input}"),
        ]
    )

    return prompt | llm

def module1_ui(api_key):
    st.header("📜 Conversational Legal Document Drafter")

    if 'drafting_history' not in st.session_state:
        st.session_state.drafting_history = []

    if 'drafting_chain' not in st.session_state:
        st.session_state.drafting_chain = setup_drafting_agent(api_key)

    for message in st.session_state.drafting_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.markdown(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.markdown(message.content)

    user_input = st.chat_input("Start drafting your document...")
    if user_input:
        st.session_state.drafting_history.append(HumanMessage(content=user_input))
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.spinner("Thinking..."):
            response = st.session_state.drafting_chain.invoke(
                {"history": st.session_state.drafting_history, "input": user_input}
            )

        st.session_state.drafting_history.append(AIMessage(content=response.content))
        with st.chat_message("assistant"):
            st.markdown(response.content)
