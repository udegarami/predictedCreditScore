import streamlit as st
import requests
import config
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np 
import json

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
    st.header('Prediction')
    apipath=config.server["path"]+"/api/v1/df"
    ids = list(json.loads(requests.get(apipath).text))
    ids = [d['id'] for d in ids]
    options = st.selectbox(
    'Select Customer by ID',
    ids)
    id_value = options#['id']
    apipath=config.server["path"]+"/api/v1/predict/"+str(id_value)
    score = json.loads(requests.get(apipath).text)
    score = json.loads(score)
    score = list(score.values())[0]
    score = score * 100
    score = round(score, 2)
    st.text("Payback probability: " + str(score) + " %")

with modelTraining: 
    st.header('Information about the customer')
    st.text('She is very smart')
    chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

    st.bar_chart(chart_data)

with devInfo:
    st.header('Information for Data Scientists')
    st.text('The Classification Model chosen is:')
    st.text('The Hyperparameters chosen are:')
    apipath=config.server["path"]+"/api/v1/image/shap_analysis.png"

    response = requests.get(apipath)
    if response.status_code == 200:
        with open("shap_analysis.png", "wb") as f:
            f.write(response.content)
        st.image("shap_analysis.png", width=600, caption="Shap Analysis")
