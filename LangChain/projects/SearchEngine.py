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

os.environ["HF_TOKEN"]=os.getenv("HF_TOKEN")

# creating embeddings
hug_embeddings=HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

# wikipedia. arxiv api wrapper
wiki_api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=300)
wikipedia=WikipediaQueryRun(api_wrapper=wiki_api_wrapper)

arxiv_api_wrapper=ArxivAPIWrapper(top_k_results=1,doc_content_chars_max=300)
arxiv=ArxivQueryRun(api_wrapper=arxiv_api_wrapper)

# it is used to search directly from the internet
search=DuckDuckGoSearchRun(name="Search")

st.title("Langchain-Chat with Search")
"""
In this example, we are using 'StreamlitCallbackHandler' to display the thoughts and actions of an agent in an interactive streamlit app.
https://github.com/langchain-ai/streamlit-agent?tab=readme-ov-file
"""

groq_api_key=st.sidebar.text_input("Enter Groq Api Key", type="password")

# streamlit session state
if 'messages' not in st.session_state:
    st.session_state['messages']=[
        {"role":"assistant","content":"Hi, I'm a chatbot who can search the web. How may I help you ?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])

if groq_api_key:
    if prompt:=st.chat_input(placeholder="Type message here"):
        st.session_state.messages.append({'role':"user","content":prompt})
        st.chat_message("user").write(prompt)

        # creating llm
        groq_llm=ChatGroq(model='Llama3-8b-8192',groq_api_key=groq_api_key,streaming=True)

        tools=[wikipedia,arxiv,search]

        search_agent=initialize_agent(tools,groq_llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

        with st.chat_message("assistant"):
            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=search_agent.run(st.session_state.messages, callbacks=[st_cb])
            st.session_state.messages.append({'role':'assistant','content':response})
            st.write(response)