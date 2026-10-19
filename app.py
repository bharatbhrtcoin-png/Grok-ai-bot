import os
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Grok AI Bot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 Grok AI Bot")
st.caption("AI chatbot powered by a free LLM API")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask anything...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a helpful, intelligent AI assistant. "
                            "Answer clearly and accurately. "
                            "You can communicate in Hindi, Hinglish and English."
                        )
                    },
                    *st.session_state.messages
                ]
            )

            answer = response.choices[0].message.content
            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
