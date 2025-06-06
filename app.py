import streamlit as st
import pickle 
import pandas as pd
import numpy as np 
from sklearn.preprocessing import StandardScaler,LabelEncoder,OneHotEncoder
import tensorflow as tf 


#loading the trained model
model = tf.keras.models.load_model('model.h5')

with open('label_encoder_gender.pkl','rb') as file:
    label_encoder_gender = pickle.load(file)
    
with open('onehot_encoder_geo.pkl','rb') as file:
    onehot_encoder_geo = pickle.load(file)
    
with open('scalar.pkl','rb') as file:
    scalar = pickle.load(file)
    
    
# Streamlit app

st.title("Customer Churn Prediction")

# User input
geography = st.selectbox('Geography', onehot_encoder_geo.categories_[0])
gender = st.selectbox('Gender', label_encoder_gender.classes_)
age = st.number_input('Age', 18,95)
balance = st.number_input('Balance')
credit_score =  st.number_input('Credit Score' )
estimated_salary = st.number_input('Estimated Salary')
tenure = st.slider('Tenure', 0,10)
num_of_products = st.slider('Number of Products', 1,4)
has_credit_card = st.selectbox('Has Credit Card', [0, 1])
is_active_member = st.selectbox('Is Active Member', [0, 1])


# Preprocess user input
input_data = pd.DataFrame({
    'CreditScore': [credit_score],
    'Gender': [label_encoder_gender.transform([gender])[0]],
    'Age': [age],
    'Tenure': [tenure],
    'Balance': [balance],
    'NumOfProducts': [num_of_products],
    'HasCrCard': [has_credit_card],
    'IsActiveMember': [is_active_member],
    'EstimatedSalary': [estimated_salary]
})

geo_encoded = onehot_encoder_geo.transform([[geography]]).toarray()
geo_encoded_df = pd.DataFrame(geo_encoded, columns=onehot_encoder_geo.get_feature_names_out(['Geography']))


input_data = pd.concat([input_data.reset_index(drop=True),geo_encoded_df],axis=1)
input_data_scaled = scalar.transform(input_data)

prediction_prob = model.predict(input_data_scaled)
prediction_prob = prediction_prob[0][0]

if st.button("Preidct"):
    st.write(f"Prediction Probability: {prediction_prob}")
    if prediction_prob > 0.5:
        st.write("Customer will leave the bank")
        
    else:
        st.write("Customer will not leave the bank")
        

