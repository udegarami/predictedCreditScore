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
    prediction = requests.get(apipath).json()
    #st.bar_chart(data= prediction,x= prediction["id"] , y= prediction["score"])
    st.text(prediction)
    st.write(prediction)
    import pandas as pd
    import numpy as np

    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

    st.bar_chart(chart_data)