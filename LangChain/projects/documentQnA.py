# Application in user user can upload any pdf file and will able to query that document

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.output_parsers import StrOutputParser


pdf=st.sidebar.file_uploader("Upload PDF file:", type='pdf')

# loading the pdf
loader=PyPDFLoader(pdf)
pdf_loader=loader.load()

# creating chunks
txt_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
pdf_chunks=txt_splitter.split_documents(pdf_loader)

# creating embeddings
hugg_embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# creating vector and storing
faiss_db=FAISS.from_documents(pdf_chunks,hugg_embeddings)