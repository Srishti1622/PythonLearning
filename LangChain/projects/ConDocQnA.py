# RAG conversational document QnA with chat history

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder


load_dotenv()

os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

# getting api key from user 
api_key=st.sidebar.text_input("Enter Groq API Key here", type="password")


def get_session_history(session_id: str)-> BaseChatMessageHistory:
    if session_id not in st.session_state.store:
        st.session_state.store[session_id]=ChatMessageHistory()
    return st.session_state.store[session_id]

# contextual system prompt
context_system_prompt=(
    "Given a chat history and the latest user question"
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood"
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

# prompt
prompt=ChatPromptTemplate.from_messages(
    [
        ("system",context_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human","{input}"),
    ]
)

# question asking prompt
qa_system_prompt=(
    "You are an assistant for question-answering tasks."
    "Use the following pieces of retrieved context to answer"
    "the question. If you don't know the answer, say that you"
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

qa_prompt=ChatPromptTemplate.from_messages(
    [
        ("system",qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human","{input}"),
    ]
)

if api_key:
    # creating llm model using groq
    llm=ChatGroq(model="Gemma2-9b-It",groq_api_key=api_key)

    # creating embeddings using huggingface
    embeddings=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # getting session id from user and if not provided then keeping it default value
    session_id=st.sidebar.text_input("Current Session Id",value="sri16")

    # creating store dict for storing session id
    if 'store' not in st.session_state:
        st.session_state.store={}

    # getting pdf uploaded by user
    pdf=st.sidebar.file_uploader("Provide PDF",type="pdf")

    if pdf:
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

        # creating retriever
        retriever=faiss_vector.as_retriever()

        # deleting the file from temporary location
        if os.path.exists("temp_uploaded_file.pdf"):
            os.remove("temp_uploaded_file.pdf")

        st.title("Conversational DocQnA")
        question=st.text_input("Query the uploaded pdf")

        if question:
            # this retriever will have the chat history 
            history_aware_retriever=create_history_aware_retriever(llm,retriever,prompt)

            qa_chain=create_stuff_documents_chain(llm,qa_prompt)

            rag_chain=create_retrieval_chain(history_aware_retriever,qa_chain)

            conversational_rag_chain=RunnableWithMessageHistory(
                rag_chain,
                get_session_history,
                input_messages_key="input",
                history_messages_key="chat_history",
                output_messages_key="answer"
            )

            session_history=get_session_history(session_id)

            response=conversational_rag_chain.invoke(
                {'input':question},
                config={
                    "configurable":{"session_id":session_id}
                }
            )

            st.write(st.session_state.store)
            st.write("Answer:", response['answer'])
            st.write("chat_history:", session_history.messages)

else:
    st.sidebar.warning("Please provide api key to continue")