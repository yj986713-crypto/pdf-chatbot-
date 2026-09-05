import streamlit as st
import PyPDF2

st.set_page_config(page_title="PDF Chatbot by Yash")
st.title("PDF Chatbot for BSc Notes - by Yash")

st.markdown("**BSc AI Student | Goal: Rakuten Japan Internship 2027**")

pdf_file = st.file_uploader("Apna BSc ka PDF yaha daalo", type="pdf")

if pdf_file:
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    
    st.success(f"PDF padh liya! {len(reader.pages)} pages hai.")
    
    question = st.text_input("Ab is notes se kya puchhna hai?")
    if question:
        st.write("Tera sawal:", question)
        # Simple search - aage isme AI lagayenge
        if question.lower() in text.lower():
            st.write("Jawab notes me mila! ✅")
        else:
            st.write("Iska jawab notes me dhoondh raha hu...")
        st.text_area("Notes ka content:", text[:2000])
