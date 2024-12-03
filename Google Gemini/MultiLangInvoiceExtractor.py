# user can upload the invoice in any language and extract the details

from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# loading the evironment variables from .env file
load_dotenv()

# configure the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# creating model
model=genai.GenerativeModel('gemini-1.5-pro')

# function to pass input and get response
def get_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

# passing the immage and converting it into bytes and returning
def image_setup(uploaded_image):
    if uploaded_image is not None:
        # read the image into bytes
        bytes_data=uploaded_image.getvalue()
        image_parts=[
            {
                "mime_type":uploaded_image.type,
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# streamlit setup
st.set_page_config(page_title="Multi-Language Invoice Extractor")
st.header("Multi-Language Invoice Extractor")

# getting input image from user
input=st.text_input("Ask you question")
uploaded_image=st.file_uploader("Upload an invoice image", type=['jpg','jpeg','png'])
image=''
if uploaded_image is not None:
    image=Image.open(uploaded_image)
    st.image(image,caption="Invoice",use_container_width=True)

ask=st.button("Tell me about the invoice")

prompt="""You are an expert in understanding invoices. 
You will be provided with an image of invoice and you need to answer the question user asked based on the uploaded invoice image.
"""

if ask:
    image_data=image_setup(uploaded_image)
    response=get_response(prompt,image_data,input)
    st.success(response)