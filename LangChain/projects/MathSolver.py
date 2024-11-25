# Application to any text to maths solver for any math related problem 

# need to install - pip install numexpr - for LLMMathChain
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

# initializing the tools
wiki_wrapper=WikipediaAPIWrapper()
wiki_tool=Tool(
    name="Wikipedia",
    func=wiki_wrapper.run,
    description="A tool for searching the internet to find the vations infomation on the topic mentioned"
)

# initialize the math tool
math_chain=LLMMathChain.from_llm(llm=groq_llm)
calculator=Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math related questions. Only input mathematical expression need to be provided"
)

# creating prompt template
prompt_template=""" 
You are a agent tasked for solving mathematical question.Logically arrive at the solution and provide a detailed explanation and display it point wise for the question below.
Question:{question}
Answer:
"""
prompt=PromptTemplate(
    input_variables=['question'],
    template=prompt_template
)

# combine all the tools into chain
chain=LLMChain(llm=groq_llm,prompt=prompt)

reasoning_tool=Tool(
    name="Reasoning Tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions"
)

# initialize the agent
assistant_agent=initialize_agent(
    tools=[wiki_tool,calculator,reasoning_tool],
    llm=groq_llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_error=True
)

if "messages" not in st.session_state:
    st.session_state['messages']=[{'role':'assistant','content':"Hi, I'm a Math Chatbot."}]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])


# getting question from user
question=st.text_input("Ask your question here")

if st.button("Solve"):
    if question:
        with st.spinner("Generating response..."):
            st.session_state.messages.append({'role':'user','content':question})
            st.chat_message('user').write(question)

            st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
            response=assistant_agent.run(st.session_state.messages,callbacks=[st_cb])
            st.session_state.messages.append({'role':'assistant','content':response})
            st.success(response)

    else:
        st.warning("Please provide the question")