import streamlit as st
import requests
import config

header = st.container()
dataset = st.container()
features = st.container()
modelTraining = st.container()
test = st.container()

with header: 
    st.title('Loan Payback Estimator')

with dataset: 
    st.header('Banking Data')
    st.text('Find the Dataset @ URL: ')

with features: 
    st.header('Features')

with modelTraining: 
    st.header('Test')
    st.text('The Hyperparameters are')
    apipath=config.server["path"]+"/api/v1/predictions/2"
    data = requests.get(apipath).json()
    st.text(data)
    st.write(data)