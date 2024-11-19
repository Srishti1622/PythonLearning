# RAG conversational document QnA with chat history

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS

# getting api key from user 
api_key=st.sidebar.text_input("Enter Groq API Key here", type="password")


if api_key:
    # creating llm model using groq
    llm=ChatGroq(model="Gemma2-9b-It",groq_api_key=api_key)

    # creating embeddings using huggingface
    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # getting session id from user and if not provided then keeping it default value
    session_id=st.sidebar.text_input("Current Session Id",value="sri16")

    # getting pdf uploaded by user
    pdf=st.sidebar.file_uploader("Provide PDF",type="pdf")

    # Save the uploaded file to a temporary location
    with open("temp_uploaded_file.pdf", "wb") as f:
        f.write(pdf.getbuffer())
    
    # loading the pdf
    loader=PyPDFLoader("temp_uploaded_file.pdf")
    pdf_loader=loader.load()

    # creating chunks
    txt_splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)
    chunks=txt_splitter.split_documents(pdf_loader)

    # creating vector and storing in faiss
    faiss_vector=FAISS.from_documents(pdf_loader,embeddings)
