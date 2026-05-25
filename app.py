import streamlit as st
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORT_EMAIL = os.getenv('SUPPORT_EMAIL', 'support@example.com')

try:
    from src.agent import get_answer
except ImportError:
    st.error("Error importing agent module")
    st.stop()

st.set_page_config(
    page_title="BIA_Capstone_Final",
    page_icon="🛍️",
    layout="wide"
)

with st.sidebar:
    st.title("⚙️ Agent Dashboard")
    st.markdown("---")
    st.success("🟢 Gemini AI Agent Live")
    st.info("🧠 Model: Gemini 2.5 Flash")
    st.markdown("### Features")
    st.markdown("- 📚 RAG: Knowledge Base")
    st.markdown("- 🛠️ Tool: Order Status")
    st.markdown("- 🛠️ Tool: Return Request")
    st.markdown("- 🛡️ Safety: Human Escalation")

st.title("🛍️ BIA_Capstone_Final")
st.subheader("E-Commerce Customer Support Assistant")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Ask me anything about our store:")

if user_input:
    if len(user_input.strip()) < 3:
        st.warning("⚠️ Please ask a more detailed question")
    else:
        with st.chat_message("user"):
            st.write(user_input)
        
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })
        
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = get_answer(user_input)
                    st.write(response)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    response = f"Error. Contact {SUPPORT_EMAIL}"
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        logger.info(f"Query: {user_input}")

st.divider()
st.markdown(f"""
<div style="text-align: center; color: #999; font-size: 0.85em;">
    💬 Try: "How much is shipping?" or "Order status 12345"
    
    📧 Support: {SUPPORT_EMAIL}
</div>
""", unsafe_allow_html=True)
