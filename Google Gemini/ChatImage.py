# Google Gemini model to pass image along with some text or only image

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# loading the environment variables
load_dotenv()

# setting up the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# creating llm model
# "gemini-pro-vision" is not present now 
# model=genai.GenerativeModel("gemini-pro-vision")
# "gemini-1.5-flash" is take both text and image
model=genai.GenerativeModel("gemini-1.5-flash")

# function to call llm model and get the response based on passed question
def get_response(input,image):
    # this .generate_content() method is used to pass the input to llm model
    if input!="":
        response=model.generate_content([input,image])
    else:
        response=model.generate_content(image)
    return response.text

# streamlit setup
st.set_page_config(page_title="Gemini Image Demo")

st.header("Google Gemini Image Application")

input=st.text_input("Ask your question")

# getting image from user
uploaded_image=st.file_uploader("Choose an image...",type=['jpg','jpeg','png'])
image=''
if uploaded_image is not None:
    image=Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)
ask=st.button("Tell me about image")

if ask and not image:
    st.warning("Please provide image!")

if ask and image:
    response=get_response(input,image)
    st.write(response)