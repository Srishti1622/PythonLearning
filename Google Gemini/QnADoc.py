# Document QnA using Google Gemma and Grop API

import time
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# loading environment variables from .env file
load_dotenv()

# setting up the api keys
os.environ['GROQ_API_KEY']=os.getenv('GROQ_API_KEY')
os.environ['GOOGLE_API_KEY']=os.getenv('GOOGLE_API_KEY')

st.title("Doc QnA - Gemma Model")

# creating llm model
groq_llm=ChatGroq(model='Gemma-7b-It')

# creating prompt
prompt=ChatPromptTemplate.from_template(
    """
Answer the question based on the provided context only.
Please provide the most accurate reponse based on the question
<context>
{context}
<context>
Question: {input}
"""
)

# function to create vector store
def vector_embedding():
    if 'vectors' not in st.session_state:
        st.session_state.embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        st.session_state.loader=PyPDFDirectoryLoader('../LangChain/files')   # data ingestion
        st.session_state.docs=st.session_state.loader.load()
        st.session_state.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=500)
        st.session_state.final_docs=st.session_state.text_splitter.split_documents(st.session_state.docs)
        st.session_state.vectors=FAISS.from_documents(st.session_state.final_docs,embedding=st.session_state.embeddings)

input=st.text_input("Ask you question!")

if st.button("Create vector store"):
    vector_embedding()
    st.write("Vector store created!")

if input:
    doc_chain=create_stuff_documents_chain(groq_llm,prompt)
    retriever=st.session_state.vectors.as_retriever()
    retriever_chain=create_retrieval_chain(retriever,doc_chain)

    start=time.process_time()
    response=retriever_chain.invoke({'input':input})
    st.write(response['answer'])

    with st.expander("Document similarity search"):
        for i, doc in enumerate(response['context']):
            st.write(doc.page_content)
            st.write("==================")