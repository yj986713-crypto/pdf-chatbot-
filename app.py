import streamlit as st
import pypdf
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from groq import Groq

st.set_page_config(page_title="DocuMind - YC Ready", layout="wide")
st.title("🧠 DocuMind - AI PDF Engineer")
st.caption("Built for YC W24 Internship | RAG + Quiz Generator")

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

model = load_model()
client = Groq(api_key=st.secrets["GROQ_API_KEY"]) # Free API

pdf = st.file_uploader("PDF upload kar (Notes, Book)", type="pdf")

if pdf:
    reader = pypdf.PdfReader(pdf)
    full_text = "".join([p.extract_text() or "" for p in reader.pages])

   
    chunks = [full_text[i:i+500] for i in range(0, len(full_text), 400)]
    st.success(f"Processed: {len(reader.pages)} pages | {len(chunks)} chunks")

    embeddings = model.encode(chunks)

    
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings).astype('float32'))

    tab1, tab2 = st.tabs(["💬 Chat with PDF", "📝 Generate Quiz (YC Feature)"])

    with tab1:
        q = st.text_input("Ask question from PDF")
        if q:
            q_emb = model.encode([q])
            D, I = index.search(np.array(q_emb).astype('float32'), 3)
            context = "\n".join([chunks[i] for i in I[0]])

            # LLM
            prompt = f"Context: {context}\n\nQuestion: {q}\nAnswer in simple points:"
            res = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role":"user", "content": prompt}]
            )
            st.write(res.choices[0].message.content)

    with tab2:
        if st.button("Generate MCQ Quiz from PDF"):
            context = "\n".join(chunks[:3])
            prompt = f"From this text, create 5 MCQ quiz with answer: {context}"
            res = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role":"user", "content": prompt}]
            )
            st.write(res.choices[0].message.content)
