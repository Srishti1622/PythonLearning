# Google Gemini model to pass image along with some text or only image

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# loading the environment variables
load_dotenv()

# setting up the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# creating llm model
model=genai.GenerativeModel("gemini-pro-vision")

# function to call llm model and get the response based on passed question
def get_response(input,image):
    # this .generate_content() method is used to pass the input to llm model
    if input!="":
        response=model.generate_content([input,image])
    else:
        response=model.generate_content(image)
    return response.text
