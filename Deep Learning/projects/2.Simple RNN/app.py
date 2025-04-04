import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.datasets import imdb
import streamlit as st

# Load the pre-trained model with ReLU activation
model=load_model(r'C:\Users\srish\PythonLearning\Deep Learning\projects\2.Simple RNN\Simple_RNN_movie_review_prediction.h5')

# Load the IMDB dataset word index
word_index = imdb.get_word_index()

# Step 2: Helper Functions
# Function to preprocess user input
def preprocess_text(text):
    words = text.lower().split()
    encoded_review = [word_index.get(word, 2) + 3 for word in words]
    padded_review = pad_sequences([encoded_review], maxlen=500)
    return padded_review

# Streamlit app
st.title('IMDB Movie Review Sentiment Analysis')
st.write('Enter a movie review to classify it as positive or negative.')

# User input
user_input = st.text_area('Movie Review')

if st.button('Classify'):

    preprocessed_input=preprocess_text(user_input)

    ## Make prediction
    prediction=model.predict(preprocessed_input)
    sentiment='Positive' if prediction[0][0] > 0.5 else 'Negative'

    # Display the result
    st.write(f'Sentiment: {sentiment}')
    st.write(f'Prediction Score: {prediction[0][0]}')
else:
    st.write('Please enter a movie review.')