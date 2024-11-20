# Search Engine using tools and agents

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.tools import WikipediaQueryRun,ArxivQueryRun,DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain.agents import initialize_agent,AgentType
from langchain.callbacks import StreamlitCallbackHandler

load_dotenv()

os.environ["HF_TOEKN"]=os.getenv("HF_TOEKN")

# creating llm
groq_llm=ChatGroq(model='Llama3-8b-8192')

# creating embeddings
hug_embeddings=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# wikipedia. arxiv api wrapper
wiki_api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=300)
wikipedia=WikipediaQueryRun(api_wrapper=wiki_api_wrapper)

arxiv_api_wrapper=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=300)
arxiv=ArxivQueryRun(api_wrapper=arxiv_api_wrapper)

groq_api_key=st.sidebar.text_input("Enter Groq Api Key", type="password")