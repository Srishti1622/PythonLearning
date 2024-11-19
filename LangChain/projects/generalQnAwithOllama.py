import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.llms import Ollama
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# LangSmith tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"

# creating llm
ollama_llm=OllamaLLM(model="llama3")

# creating prompt
ollama_prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Please respond to the question asked."),
        ("user","{question}")
    ]
)

# streamlit ui
st.title("Langchain with Ollama")
input_question=st.text_input("What question you have in your mind?")

# output parser creating
output_parser=StrOutputParser()

chain=ollama_prompt|ollama_llm|output_parser

if input_question:
    st.write(chain.invoke({input_question}))
