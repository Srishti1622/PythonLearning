import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle
import pandas as pd
import numpy as np
import streamlit as st

# loading the modela dn pickle files
model=load_model(r'C:\Users\srish\PythonLearning\Deep Learning\projects\1.Simple ANN\regression\model_reg.h5')

with open(r'C:\Users\srish\PythonLearning\Deep Learning\projects\1.Simple ANN\classification\labelencoder.pkl','rb') as file:
    labelencoder=pickle.load(file)

with open(r'C:\Users\srish\PythonLearning\Deep Learning\projects\1.Simple ANN\classification\onehotencoder.pkl','rb') as file:
    onehotencoder=pickle.load(file)

with open(r'C:\Users\srish\PythonLearning\Deep Learning\projects\1.Simple ANN\regression\scaler.pkl','rb') as file:
    scaler=pickle.load(file)

# streamlit ui
st.title("Estimated Salary Prediction")

# user input
geography = st.sidebar.selectbox('Geography', onehotencoder.categories_[0])
gender = st.sidebar.selectbox('Gender', labelencoder.classes_)
age = st.sidebar.slider('Age', 18, 92)
balance = st.sidebar.number_input('Balance')
credit_score = st.sidebar.number_input('Credit Score')
tenure = st.sidebar.slider('Tenure', 0, 10)
num_of_products = st.sidebar.slider('Number of Products', 1, 4)
has_cr_card = st.sidebar.selectbox('Has Credit Card', [0, 1])
is_active_member = st.sidebar.selectbox('Is Active Member', [0, 1])
exited = st.sidebar.selectbox('Is Exited', [0, 1])

# input data
df=pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [labelencoder.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_cr_card],
    'IsActiveMember': [is_active_member],
    'Exited': [exited]
})

geo=onehotencoder.transform([[geography]]).toarray()
geo_df=pd.DataFrame(geo,columns=onehotencoder.get_feature_names_out())

df=pd.concat([df.reset_index(drop=True),geo_df],axis=1)

if not df.empty:
    scaled_df=scaler.transform(df)
    prediction=model.predict(scaled_df)
    st.write(f'Customer Salary based on selection: {prediction[0][0]:.2f}')