import streamlit as st
import PyPDF2

st.title("PDF Chatbot - Yash")
st.caption("Goal: Rakuten India Bangalore Internship 2026")

pdf = st.file_uploader("PDF upload kar", type="pdf")

if pdf:
    reader = PyPDF2.PdfReader(pdf)
    full_text = ""
    for p in reader.pages:
        full_text += (p.extract_text() or "") + "\n"
    
    st.success(f"PDF read ho gaya - {len(reader.pages)} pages")
    
    q = st.text_input("Question puch (ex: What is Class?)")
    
    if q:
        keywords = [w for w in q.lower().split() if len(w)>3]
        lines = [l for l in full_text.split("\n") if any(k in l.lower() for k in keywords)]
        
        if lines:
            st.subheader("Answer from notes:")
            for l in lines[:5]:
                st.write(f"- {l}")
        else:
            st.error("Ye topic is PDF me hai hi nahi. Dusra question puch jaise 'What is Class?'")
