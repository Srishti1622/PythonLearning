# RAG conversational document QnA with chat history

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq


api_key=st.sidebar.text_input("Enter Groq API Key here", type="password")


if api_key:
    llm=ChatGroq(model="Gemma2-9b-It",groq_api_key=api_key)

    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    session_id=st.sidebar.text_input("Current Session Id",value="sri16")

    pdf=st.sidebar.file_uploader("Provide PDF")
