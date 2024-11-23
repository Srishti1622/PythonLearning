# An application in which we are connect and querying both local db as well as mysql database 

import streamlit as st
from pathlib import Path
from sqlalchemy import create_engine
import sqlite3
# Construct a SQL agent from an LLM and toolkit or database
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.callbacks import StreamlitCallbackHandler
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain_groq import ChatGroq


st.set_page_config(page_title="LangChain: Chat with SQL DB")
st.title("Chat with SQL DB")

LOCALDB='USE_LOCALDB'
MYSQL='USE_MYSQL'

radio_opt=['Use SQLite3', 'Use MYSQL']
selected_opt=st.sidebar.radio(label="Choose the DB to chat",options=radio_opt)

if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Enter Host")
    mysql_user=st.sidebar.text_input("Enter User")
    mysql_password=st.sidebar.text_input("Enter Password",type="password")
    mysql_db=st.sidebar.text_input("Enter Database")
else:
    db_uri=LOCALDB


api_key=st.sidebar.text_input("Enter Groq API Key",type="password")

if not db_uri:
    st.info("Please provide the database info")

if not api_key:
    st.info("Please provide api key")

# this decorator is for caching as we don't need to connect each time to db
# ttl= total time limit
@st.cache_resource(ttl='2h')
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        # setup the filepath to local db here 'student.db'
        db_filepath=(Path(__file__).parent/"student.db").absolute()
        print(db_filepath)
        # creating a creator to connect to sqlite database in read only mode
        creator=lambda: sqlite3.connect(f"file:{db_filepath}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MYSQL details")
            st.stop()
        # this is how we connect to MYSQL database
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))
    

if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db=configure_db(db_uri)


if api_key:
    # creating llm model
    groq_llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)
    # toolkit:
    toolkit=SQLDatabaseToolkit(db=db,llm=groq_llm)

    agent=create_sql_agent(
        llm=groq_llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )

    # for maintaining the chat history
    if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
        st.session_state["messages"]=[{'role':'assistant','content':'How can I help you?'}]

    for msg in st.session_state.messages:
        st.chat_message(msg['role']).write(msg['content'])

    user_query=st.chat_input(placeholder="Ask anything from the database")

    if user_query:
        # appending each conversation to session state
        st.session_state.messages.append({'role':'user','content':user_query})
        # adding in chat messages to show in the screen
        st.chat_message('user').write(user_query)

        # this is to display each processing of llm
        with st.chat_message('assistant'):
            streamlit_callback=StreamlitCallbackHandler(st.container())
            response=agent.run(user_query,callbacks=[streamlit_callback])
            # adding the llm response to session state
            st.session_state.messages.append({'role':'assistant','content':response})
            st.write(response)