# app.py
import streamlit as st
from langchain.document_loaders import TextLoader
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Load and embed
loader = TextLoader("reviews.txt")
docs = loader.load()
db = Chroma.from_documents(docs, HuggingFaceEmbeddings())

qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(
        model_name="mistralai/mistral-7b-instruct",
        openai_api_key=OPENAI_API_KEY,
        openai_api_base="https://openrouter.ai/api/v1",
    ),
    retriever=db.as_retriever()
)

st.title("💬 Ask Me About My Customers")
query = st.text_input("Ask a question based on customer reviews")

if query:
    answer = qa_chain.run(query)
    st.write("🤖", answer)
