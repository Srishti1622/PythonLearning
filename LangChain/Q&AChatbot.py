import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# loading environment variables
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]="Q&A chatbot with Groq"
os.environ["LANGCHAIN_TRACING_V2"]="true"

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Answer the provided question to best of your ability"),
        ("human","{question}")
    ]
)

output_parser=StrOutputParser()

groq_api_key=st.sidebar.text_input("Enter Groq Api key",type="password")
model=st.sidebar.selectbox("Select Groq Model",["Gemma2-9b-It","Llama3-8b-8192"])
temperature=st.sidebar.slider("Provide temperature",min_value=0.0,max_value=1.0,value=0.25)
token=st.sidebar.slider("Provide token count",min_value=50,max_value=300,value=150)

st.title("QnA Chatbot using Groq")
groq_llm=ChatGroq(
    model=model,
    groq_api_key=groq_api_key,
    temperature=temperature,
    max_tokens=token
)
chain=prompt|groq_llm|output_parser
question=st.text_input("What's in your mind?")
if question:
    st.write(chain.invoke({"question":question}))




