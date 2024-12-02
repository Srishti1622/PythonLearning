# Google Gemini for text based chatbot where user can ask any question and get the response

from dotenv import load_dotenv
import streamlit
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