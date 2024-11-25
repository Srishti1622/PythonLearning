# Application to any text to maths solver for any math related problem 

import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMChain, LLMMathChain
from langchain.prompts import PromptTemplate
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler

# streamlit app setup
st.set_page_config(page_title="Text to Math Solver")
st.title("Text to Math Solver")

# taking api key from user
api_key=st.sidebar.text_input("Enter Groq API Key", type="password")

# if api key not provided
if not api_key:
    st.info("Please provide Groq API Key to continue")
    st.stop()

# creating llm model
groq_llm=ChatGroq(model="Gemma2-9b-It",groq_api_key=api_key)

#