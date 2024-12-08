import streamlit as st
import time
import random
from datetime import datetime

# Page config
st.set_page_config(layout="wide", initial_sidebar_state='collapsed')

# Custom CSS with Claude-like styling
css = """
<style>
    /* Main container styling */
    .main {
        font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* Chat container */
    .chat-container {
        padding: 20px;
        margin-bottom: 60px;
        font-size: 16px;
        line-height: 1.5;
    }

    /* Message styling */
    .message {
        padding: 15px 20px;
        margin: 10px 0;
        border-radius: 5px;
        max-width: 90%;
    }

    .user-message {
        background-color: #f3f3f3;
        margin-left: auto;
        margin-right: 0;
    }

    .assistant-message {
        background-color: #ffffff;
        border: 1px solid #e1e1e1;
        margin-right: auto;
    }

    /* Artifact styling */
    .artifact-container {
        background-color: #ffffff;
        border: 1px solid #e1e1e1;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }

    .artifact-header {
        font-size: 14px;
        color: #666;
        margin-bottom: 10px;
        padding-bottom: 5px;
        border-bottom: 1px solid #e1e1e1;
    }

    /* Chat header */
    .chat-header {
        font-size: 24px;
        font-weight: 500;
        color: #1a1a1a;
        margin-bottom: 20px;
        padding: 20px 0;
        border-bottom: 1px solid #e1e1e1;
    }

    /* Input area */
    .input-area {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding: 20px;
        border-top: 1px solid #e1e1e1;
    }

    /* Streaming effect */
    .streaming {
        opacity: 0.7;
    }

    @keyframes blink {
        0% { opacity: 1; }
        50% { opacity: 0; }
        100% { opacity: 1; }
    }

    .cursor {
        display: inline-block;
        width: 2px;
        height: 16px;
        background: #666;
        animation: blink 1s infinite;
    }
</style>
"""

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_title" not in st.session_state:
    st.session_state.chat_title = f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}"


def dummy_stream_generator(prompt: str) -> str:
    """Simulate streaming response."""
    responses = [
        f"Let me analyze your question about {prompt}...",
        "Based on my understanding, I can provide the following insights:",
        "Here are some key points to consider:",
        "To elaborate further on this topic:"
    ]
    base_response = random.choice(responses)
    words = base_response.split()

    for word in words:
        yield word + " "
        time.sleep(0.1)


# Render the custom CSS
st.markdown(css, unsafe_allow_html=True)

# Create two columns: chat and artifact
col1, col2 = st.columns([0.6, 0.4])

with col1:
    # Chat header
    st.markdown(f'<div class="chat-header">{st.session_state.chat_title}</div>', unsafe_allow_html=True)

    # Chat messages container
    chat_container = st.container()

    # Display chat history
    with chat_container:
        for msg in st.session_state.messages:
            role_class = "user-message" if msg["role"] == "user" else "assistant-message"
            st.markdown(
                f'<div class="message {role_class}">{msg["content"]}</div>',
                unsafe_allow_html=True
            )

with col2:
    # Artifact area
    st.markdown("""
        <div class="artifact-container">
            <div class="artifact-header">Artifact Area</div>
            <div id="artifact-content"></div>
        </div>
    """, unsafe_allow_html=True)

# Input area at the bottom
input_placeholder = st.empty()
with input_placeholder.container():
    if prompt := st.chat_input("How can I help you today?", key="chat_input"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Create placeholder for streaming response
        message_placeholder = st.empty()

        # Initialize response accumulator
        full_response = ""

        # Stream the response
        for chunk in dummy_stream_generator(prompt):
            full_response += chunk
            # Display current response with blinking cursor
            message_placeholder.markdown(
                f'<div class="message assistant-message streaming">{full_response}▌</div>',
                unsafe_allow_html=True
            )

        # Add final response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Clear streaming placeholder and rerun to update chat history
        message_placeholder.empty()
        st.rerun()

# Add some spacing at the bottom for the fixed input area
st.markdown("<div style='height: 100px'></div>", unsafe_allow_html=True)