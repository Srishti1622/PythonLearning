# Application to translate text from english into another language.
# Simple application with just a single LLM call and some prompting
# In this, I have used Qroq
# Reference: https://python.langchain.com/docs/integrations/chat/groq/

# LangServe: helps developers deploy LangChain runnables and chains as a RestAPI
# this library is integrated with FastAPI and uses pydantic for data validation


import os 
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage,SystemMessage

load_dotenv()

os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
# langsmith tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")
os.environ["LANGCHAIN_TRACING_V2"]="true"

# creating llm using groq
llm=ChatGroq(model="Gemma2-9b-It")

# creating prompt using chatprompttemplate .from_template
# prompt=ChatPromptTemplate.from_template(
#     """ 
# Translate the following {input} from English to {lang}.

# """
# )

# creating prompt using chatprompttemplate .from_messages
prompt=ChatPromptTemplate.from_messages(
    [
        ("system","Translate the following from english to {lang}"),
        ("user","{input}")
    ]
)

# creating prompt using human and system messages
# prompt_directly=[
#     SystemMessage(content="Translate the following from english to french"),
#     HumanMessage(content="hello how are you ?")
# ]

# output parser
output_parser=StrOutputParser()

chain=prompt|llm|output_parser

# when using prompt_directly
# chain_directly=llm|output_parser

st.title("Translator")
lang=st.text_input("Language")
input=st.text_input("Sentence to translate")

if lang and input:
    st.write(chain.invoke({"input":{input},"lang":{lang}}))

# st.title("static prompt using human and system messages")
# st.write(chain_directly.invoke(prompt_directly))