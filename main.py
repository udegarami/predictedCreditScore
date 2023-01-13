from typing import List
from fastapi import FastAPI
from models import User, Prediction, IdList
import csv

app = FastAPI(cors=False)

db: List[User] = [
    User(
        id=1234, 
        gender ="F", 
        carOwner = "Y"
    ),
    User(
        id=12454, 
        gender ="M", 
        carOwner = "N"
    )
]

predictions: List[Prediction] = [
]
ids: List[IdList] = [
]

#Import CSV as a DB

with open('xgboost_calibrated.csv', newline='') as csv_file:
    reader = csv.reader(csv_file)
    next(reader, None)  # Skip the header.
    # Unpack the row directly in the head of the for loop.
    for id, score in reader:
        # Convert the numbers to floats.
        score = float(score)
        # Now create the Student instance and append it to the list.
        predictions.append(Prediction(id = id, score = score))
        ids.append(IdList(id = id))

### Shap Analysis
#import shap
#import numpy as np
#import pandas as pd
#from sklearn.ensemble import RandomForestClassifier

## load your data
#data = pd.read_csv("application_train.csv")
#X = data.drop("TARGET", axis=1)
#y = data["TARGET"]

# train a model
#model = RandomForestClassifier()
#model.fit(X, y)

## explain the model's predictions using SHAP values
#explainer = shap.Explainer(model, X)
#shap_values = explainer(X)

## plot the feature importances for a single prediction
#shap.summary_plot(shap_values[0], X)




### API Endpoints 

@app.get("/root")
async def root():
    #await request()
    return {"Hello": "World"}

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.get("/api/v1/predictions")
async def fetch_predictions():
    return predictions

@app.get("/api/v1/predictions/{predictionId}")
async def fetch_prediction(predictionId: int):
    return predictions[predictionId]

@app.get("/api/v1/df")
async def df():
    return ids
