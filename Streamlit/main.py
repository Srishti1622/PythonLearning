# Reference - https://streamlit.io/components
# Reference - https://docs.streamlit.io/get-started
# Streamlit is an open source app framework for Machine Learning and Data Science projects. It allows you to create beautiful web applications with simple Python scripts.

# To run the streamlit, we need to run the command- streamlit run filename.py

import streamlit as st
import pandas as pd 
import numpy as np 

# Title of the application - title means main heading of size like h1 as if we do inspect it shows h1 tag in html
st.title("Learning Streamlit")

# display a simple text, it is p tag in html
st.write("This is a simple text")

# streamlit directly display dataframe in the form of table along with download, expand, search and more features
st.write("Here is a dataframe!")
df=pd.DataFrame({
    'A':[1,2,3,4],
    'B':[5,6,7,8],
    'C':[2,4,6,8]
})
st.write(df)

# streamlit directly display line chart along with different features
st.write("Here is your line chart!")
st.line_chart(df)

# getting input from the user, input tag in html
name=st.text_input("Enter your name here")
st.write(name,"name here")
if name:
    st.write(f"Hello, {name}")

# slider which take min, max and initial value to set
age=st.slider("Slide to your age",1,100,18)
st.write(f"You are {age} years old")

# drop-down in streamlit
options=['CSE','ME','EE','CE']
choice=st.selectbox("Choose your department",options)
st.write(f"You belong to {choice} department")

# upload files in streamlit, to specify the type of file you want to accept provide the list in type attribute 
uploaded=st.file_uploader("Choose a CSV file",type="csv")
if uploaded is not None:
    df=pd.read_csv(uploaded)
    st.write(df)
