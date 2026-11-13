import streamlit as st
from openai import OpenAI
import os

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.environ.get("GROQ_API_KEY")
)

st.title("Simple LLM Request App")
st.caption("Groq")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask the LLM something..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(        # http post to groq server (request sent)
                model="openai/gpt-oss-120b",  
                messages=st.session_state.messages,
                stream=True,
            )
            response = st.write_stream(stream)      #response
        except Exception as e:
            response = f"Error: {e}"
            st.error(response)

    st.session_state.messages.append({"role": "assistant", "content": response})