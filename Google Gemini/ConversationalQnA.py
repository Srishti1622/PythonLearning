# Conversational QnA chatbot 

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# loading environment variables
load_dotenv()

# setting up the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# creating llm model
model=genai.GenerativeModel("gemini-pro")

# storing chat history
chat=model.start_chat(history=[])

# function to pass question to model and geting the response
def get_response(question):
    response=chat.send_message(question,stream=True)
    return response

# setting up streamlit app
st.set_page_config(page_title='Conversation QnA')
st.header("Conversational QnA chatbot using Gemini")

# initialize session state for chat history if it doesn't exists
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]

# getting question from user
input=st.text_input("Ask your question")
ask=st.button("Ask")

if ask and input:
    response=get_response(input)

    # adding user input question to chat history
    st.session_state['chat_history'].append(('User',input))

    # displaying response as we keep stream=True, we'll get the response in chunks
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(('Bot',chunk.text))

    st.subheader("Chat history:")
    for role,text in st.session_state['chat_history']:
        st.write(f"{role}: {text}")