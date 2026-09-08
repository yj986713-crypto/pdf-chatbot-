import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="DocuMend-YC | Internship Project", page_icon="🤖")
st.title("🤖 DocuMend-YC - AI Document Chatbot")
st.caption("Internship Project - Ask questions from your documents")

# API Key from HF Settings
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("⚠️ GROQ_API_KEY ko Settings > Variables me add karo!")
    st.stop()

client = Groq(api_key=api_key)

# Session for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

doc_text = st.text_area("Own Document / Paste the nots here :", height=200, placeholder="Like IOT  notes, PDF  text...")

# Show old chats
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New question
if question := st.chat_input("Do you have any question about the document?"):
    if not doc_text:
        st.warning("Paste the document above first!")
    else:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("AI thinking..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": f"You are DocuMend-YC, a helpful document assistant. Answer ONLY from this document: {doc_text[:12000]}"},
                        {"role": "user", "content": question}
                    ]
                )
                ans = response.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
