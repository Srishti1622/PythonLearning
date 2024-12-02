# Google Gemini for text based chatbot where user can ask any question and get the response

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# loading the environment variables
load_dotenv()

# setting up the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# creating llm model
model=genai.GenerativeModel("gemini-pro")

# function to call llm model and get the response based on passed question
def get_response(question):
    # this .generate_content() method is used to pass the input to llm model
    response=model.generate_content(question)
    return response

# streamlit setup
st.set_page_config(page_title="QnA Demo")

st.header("Google Gemini Text Application")

input=st.text_input("Ask your question")
ask=st.button("Ask")

if ask and not input:
    st.warning("Please enter your question!")

if ask and input:
    response=get_response(input)
    st.write(response.text)