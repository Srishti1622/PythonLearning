# # Application in user user can upload any pdf file and will able to query that document

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.chains import create_retrieval_chain

load_dotenv()

# loading evironment variables
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ['HF_TOKEN']=os.getenv("HF_TOKEN")

# creating llm model
groq_llm=ChatGroq(model_name="Gemma2-9b-It")

# defining prompt
# in prompt when using create_stuff_documents_chain() and create_retrieval_chain() or related things, 
# then always use context and input as variable name nothing else
# as instead of input i tried with question or msg and was getting error 
prompt=ChatPromptTemplate.from_template(
    """ 
    Answer the question based on the provided context only.
    Please provide the most accurate response based on the question
    <context>
    {context}
    <context>
    Question:{input}

    """
)

pdf=st.sidebar.file_uploader("Upload PDF file:", type='pdf')

def create_vector_embeddings():
    # creating embeddings
    hugg_embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Save the uploaded file to a temporary location
    with open("temp_uploaded_file.pdf", "wb") as f:
        f.write(pdf.getbuffer())

    # loading the save temporary pdf
    loader=PyPDFLoader("temp_uploaded_file.pdf")
    pdf_loader=loader.load()

    # creating chunks
    txt_splitter=RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    pdf_chunks=txt_splitter.split_documents(pdf_loader)

    # creating vector and storing
    st.session_state.vectors=FAISS.from_documents(pdf_chunks,hugg_embeddings)



if pdf:
    create_vector_embeddings()
    st.sidebar.write("Uploading done, now you can query the document")

    st.title("DocumentQnA")

    user_prompt=st.text_input("Enter your query from the research paper")
    


    if user_prompt:
        # it will pass context in the prompt
        # important- always in create_stuff_documents_chain, first pass llm and then prompt
        qa_chain=create_stuff_documents_chain(groq_llm,prompt)

        retrievers=st.session_state.vectors.as_retriever()

        # creating chain 
        # important- always in create_retrieval_chain, first pass the retriever and then chain created using create_stuff_documents_chain()
        rag_chain=create_retrieval_chain(retrievers,qa_chain)

        # important- always context, input in prompt as variable nothing else 
        response=rag_chain.invoke({'input':user_prompt})

        st.write(response['answer'])

        # showing context
        with st.expander("Document Similarity Search"):
            for i,doc in enumerate(response['context']):
                st.write(doc.page_content)
                st.write('-----------------------')
