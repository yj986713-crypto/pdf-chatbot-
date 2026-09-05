import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="PDF Chatbot by Yash - Rakuten 2026")

st.title("Yash")
st.write("BSc AI Student | Goal: Rakuten India Banglore Internship 2026")
st.write("Apna BSc ka PDF yaha daalo")

pdf_file = st.file_uploader("PDF upload karo", type="pdf")

if pdf_file:
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    st.success(f"PDF padh liya! {len(reader.pages)} pages hai.")

    if not text.strip():
        st.error("Ye PDF photo wala hai! Isme se text nahi nikal raha. Koi dusra PDF try karo jisme text select hota ho.")
        st.stop()

    question = st.text_input("Ab is notes se kya puchhna hai?")

    if question:
        st.write(f"Tera sawal: {question}")
        st.write("Iska jawab notes me dhoondh raha hu...")
        
        # Simple search - jo line me question ka word ho wo dikhao
        st.subheader("Notes ka content:")
        if question.lower() in text.lower():
            st.write(text[:2000])  # pehle 2000 letters dikhayega
        else:
            st.write("Is sawal ka exact jawab notes me nahi mila, par ye raha notes ka summary:")
            st.write(text[:2000])
