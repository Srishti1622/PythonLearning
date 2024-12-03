# Chat with multiple PDF documents using Langchain and Gemini pro

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate


# loading the environment variables from .env file
load_dotenv()

# setting up api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# reading pdfs and convert into text
def get_pdf_text(pdf_docs):
    text=''
    for pdf in pdf_docs:
        pdf_reader=PdfReader(pdf)
        for page in pdf_reader.pages:
            text+=page.extract_text()
    return text

# creating chunks
def get_text_chunks(text):
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=500)
    chunks=text_splitter.split_text(text)
    return chunks

# converting chunks to vector store
def get_vectorstores(chunks):
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstores=FAISS.from_texts(chunks,embedding=embeddings)

    # saving vector store in local system inside mentioned folder
    vectorstores.save_local('faiss_index')

def get_conversational_chain():
    prompt_template="""
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, 
    if the answer is not in provided context just say, "answer is not available in the context", don't provide the wrong answer \n\n
    Context:\n {context} \n
    Question:\n {question} \n
    Answer:
    """

    # creating llm model
    model=ChatGoogleGenerativeAI(
        model='gemini-pro',
        temperature=0.3
        )
    
    prompt=PromptTemplate(
        template=prompt_template,
        input_variables=['context','question']
        )
    
    chain=load_qa_chain(
        model,
        chain_type='stuff',
        prompt=prompt
    )

    return chain

# getting user input file
def user_input(question):
    embeddings=GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # loading faiss vector store from local
    new_db=FAISS.load_local('faiss_index',embeddings,allow_dangerous_deserialization=True)

    # getting context 
    docs=new_db.similarity_search(question)

    chain=get_conversational_chain()

    response=chain(
        {
            'input_documents':docs,
            'question':question
        }, return_only_outputs=True
    )

    st.write('Reply: ', response['output_text'])


# stremlit setup
def main():
    st.set_page_config("Chat with Multiple PDF")
    st.header("Chat with Multiple PDF")

    question=st.text_input("Ask your question from uploaded PDFs")

    if question:
        user_input(question)

    with st.sidebar:
        pdf_docs=st.file_uploader("Upload the pdf files",type='pdf',accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                raw_text=get_pdf_text(pdf_docs)
                text_chunks=get_text_chunks(raw_text)
                get_vectorstores(text_chunks)
                st.success("Process completed!")


if __name__=="__main__":
    main()