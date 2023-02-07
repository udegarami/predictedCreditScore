import streamlit as st
import requests
import config
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np 
import json
import plotly.express as px
import pandas as pd
import math

import os

#port = int(os.environ.get("PORT", 8501))

#Configuration page header
im = Image.open("favicon.ico")
st.set_page_config(page_title='Credit Score',layout = 'wide', initial_sidebar_state = 'auto') # page_icon = im, 

header = st.container()
prediction = st.container()
customer = st.container()
knn = st.container()
devInfo = st.container()

with header: 
    st.title('Loan Payback Estimator')

with prediction: 
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

with customer: 
    
    st.header('Information about the customer')
    marker = False
    #@st.cache
    def customerInfo(customerID):
        df=[]
        st.text("Customer ID : " + customerID)
        apipath = config.server["path"]+"/api/v1/characteristics/"+str(customerID)
        characs_text = json.loads(requests.get(apipath).text)
        characs = json.loads(characs_text)
        income_to_annuity = characs['income_to_annuity_ratio']
        proportion_life_employed = characs['proportion_life_employed']
        data=[options, income_to_annuity, proportion_life_employed]
        data_inv=[0, 0, 0]
        marker = False
        if math.isnan(proportion_life_employed) :
            marker = True
        else:
            data_inv=[0, 0, (1 - int(proportion_life_employed))]
        df= pd.DataFrame(columns=["ID","Income to Annuity Ratio","Proportion of Life employed"],data=[data,data_inv])
        ratio = pd.DataFrame(columns=["ID","Income to Annuity Ratio","Proportion of Life employed"],data=[data,data_inv])
        return df, marker

    df, marker = customerInfo(options)

    cols = st.columns([1, 1])
  
    with cols[0]:
        
        fig = px.bar(df, x= "Income to Annuity Ratio", y=1/df["Income to Annuity Ratio"],
                    title="Income to Annuity Ratio", height=300, width=200)
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)
    
    with cols[1]:
        if marker == True:
            st.text("No information to display for 'Proportion of Life employed' ")
        else:
            fig = px.pie(df, values=df["Proportion of Life employed"],
                        title="Proportion of Life employed", height=300, width=200)
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
            st.plotly_chart(fig, use_container_width=True)

with knn: 
    
    st.header('Customers with a similar profile')
    apipath=config.server["path"]+"/api/v1/neighbors/"+str(id_value)
    neighbou = json.loads(requests.get(apipath).text)
    neighbou = json.loads(neighbou)
    train = pd.read_csv('train_clean.csv')
    train = pd.DataFrame(data=train)
    neighbor_dfs = []
    for id in neighbou:
        neighbor_dfs.append(train.loc[train['SK_ID_CURR'] == id])
        neighbors = pd.concat(neighbor_dfs)

        # CSS to inject contained in a string
    hide_dataframe_row_index = """
                <style>
                .row_heading.level0 {display:none}
                .blank {display:none}
                </style>
                """
    st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)
    st.table(neighbors[['SK_ID_CURR','EXT_SOURCE_3','EXT_SOURCE_2','EXT_SOURCE_1','DAYS_EMPLOYED','AMT_INCOME_TOTAL','AMT_CREDIT','AMT_ANNUITY']])
    #st.text(neighbou)

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
