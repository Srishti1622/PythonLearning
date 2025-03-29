import tensorflow as tf
from tensorflow.keras.models import load_model
import pickle
import pandas as pd
import numpy as np
import streamlit as st

# loading the models and pickle files
model=load_model(r'C:\Users\srish\PythonLearning\Deep Learning\projects\1.Simple ANN\classification\model.h5')

with open(r'C:\Users\srish\PythonLearning\Deep Learning\projects\1.Simple ANN\classification\labelencoder.pkl','rb') as file:
    labelencoder=pickle.load(file)

with open(r'C:\Users\srish\PythonLearning\Deep Learning\projects\1.Simple ANN\classification\onehotencoder.pkl','rb') as file:
    onehotencoder=pickle.load(file)

with open(r'C:\Users\srish\PythonLearning\Deep Learning\projects\1.Simple ANN\classification\scaler.pkl','rb') as file:
    scaler=pickle.load(file)

# get the input parameters value from user using streamlit ui
st.title('Customer Churn Prediction')

# input parameters
geography=st.sidebar.selectbox('Geography',onehotencoder.categories_[0])
gender=st.sidebar.selectbox('Gender',labelencoder.classes_)
age=st.sidebar.slider('Age',18,92)
balance=st.sidebar.number_input('Balance')
credit_score=st.sidebar.number_input('Credit Score')
estimated_salary=st.sidebar.number_input('Estimated Salary')
tenure=st.sidebar.slider('Tenure',0,10)
num_of_products=st.sidebar.slider('Number of products',1,4)
has_cr_card=st.sidebar.selectbox('Has Credit Card',[0,1])
is_active_member=st.sidebar.selectbox('Is Active Member',[0,1])

input_data={
    'CreditScore':credit_score,
    'Geography':geography,
    'Gender':labelencoder.transform([gender])[0],
    'Age':age,
    'Tenure':tenure,
    'Balance':balance,
    'NumOfProducts':num_of_products,
    'HasCrCard':has_cr_card,
    'IsActiveMember':is_active_member,
    'EstimatedSalary':estimated_salary,
}

# converting the input data into dataframe
df=pd.DataFrame([input_data])

# converting the geography value to onehotencoder
geo=onehotencoder.transform([df['Geography']]).toarray()
geo=pd.DataFrame(geo,columns=onehotencoder.get_feature_names_out())

# concatenating the geo df with original df
df=pd.concat([df.drop('Geography',axis=1),geo],axis=1)

if not df.empty:
    scaled_df=scaler.transform(df)
    prediction=model.predict(scaled_df)
    if prediction[0][0]>0.5:
        st.write(f"Ohh noo! User will leave the bank {prediction[0][0]*100:.2f}%")
    else:
        st.write(f'Yahhhhh! User will stay with {prediction[0][0]*100:.2f}%')