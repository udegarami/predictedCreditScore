import streamlit as st
import requests
import config
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np

#Configuration page header
im = Image.open("favicon.ico")
st.set_page_config(page_title='Credit Score', page_icon = im, layout = 'wide', initial_sidebar_state = 'auto')

header = st.container()
dataset = st.container()
features = st.container()
modelTraining = st.container()
devInfo = st.container()

with header: 
    st.title('Loan Payback Estimator')

with features: 
    st.header('Selection')
    apipath=config.server["path"]+"/api/v1/predictions/2"
    id = requests.get(apipath).json()
    options = st.multiselect(
    'Select Customer by ID',
    #[cs_df["id"]],
    ['Green', 'Yellow', 'Red', 'Blue', id["id"]],
    ['Yellow', 'Red'])

    st.write('Selected:', options)

    duration = st.slider('Duration', 0, 35, 15)
    st.write("Mortgage duration:", duration, "years (", duration*12,"months)")

with modelTraining: 
    st.header('Prediction')
    st.text('The Hyperparameters are')
    apipath=config.server["path"]+"/api/v1/predictions/2"
    prediction = requests.get(apipath).json()
    #st.bar_chart(data= prediction,x= prediction["id"] , y= prediction["score"])
    st.text(prediction)
    st.write(prediction)


    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

    st.bar_chart(chart_data)

with devInfo:
    st.header('Information for Data Scientists')
    st.text('The Classification Model chosen is:')
    st.text('The Hyperparameters chosen are:')