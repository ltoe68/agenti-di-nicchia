import streamlit as st
import os
from dotenv import load_dotenv
from main import create_rag_chain

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Customer Support Agent", page_icon="🤖")

st.title("🤖 Customer Support Agent")
st.markdown("Ask me anything about our services!")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    provider = os.getenv("LLM_PROVIDER", "openai")
    model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
    st.info(f"**Provider:** {provider}\n\n**Model:** {model}")
    st.markdown("---")
    if st.button("Reset Conversation"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize RAG Chain (cached to avoid reloading on every rerun)
@st.cache_resource
def get_chain():
    return create_rag_chain()

chain = get_chain()

if not chain:
    st.error("Failed to initialize the AI Agent. Please check your configuration and API keys.")
    st.stop()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            with st.spinner("Thinking..."):
                response = chain.invoke(prompt)
                full_response = response['result']
                message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = f"Error: {str(e)}"
            message_placeholder.error(full_response)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
