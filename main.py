from typing import List
from fastapi import FastAPI
from models import User, Prediction, IdList
import csv
from PIL import Image
from io import BytesIO
from fastapi.responses import StreamingResponse
import joblib
import pandas as pd
import json

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

#Import CSV as a DB ######## for some reason xgboost_calibrated ids are out of bounds 

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


### API Endpoints 

@app.get("/")
def read_root():
    return {"Welcome": "to the Project"}

@app.get("/favicon.ico")
def read_favicon():
    return {"Favicon": "OK"}

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

@app.get("/api/v1/image/{file_name}")
async def read_image(file_name: str):
    try:
        img = Image.open(file_name).convert("RGBA")
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_io.seek(0)
        return StreamingResponse(img_io, media_type='image/png')
    except:
        return {"error": "could not open the image"}

# @app.get("/api/v1/predict/{predictionId}")
# async def fetch_prediction(predictionId: int):
#     calib_fit=joblib.load('calib_pipeline.joblib')
#     index=predictionId
#     # Predict default probabilities of the test data
#     test = pd.read_csv('test_encoded.csv')
#     test_pred = calib_fit.predict_proba(test.iloc[index].values.reshape(1, -1))

#     #Adding the index back
#     df_out = pd.DataFrame(columns=['SK_ID_CURR','TARGET'])
#     df_out = df_out.append({'SK_ID_CURR':index,'TARGET':test_pred[:,1][0]}, ignore_index=True)
#     return {df_out.at[0,'SK_ID_CURR']:df_out.at[0,'TARGET']}

@app.get("/api/v1/predict/{predictionId}")
async def fetch_prediction(predictionId: int):
    calib_fit=joblib.load('calib_pipeline.joblib')
    index=predictionId
    # Predict default probabilities of the test data
    test = pd.read_csv('test_encoded.csv')
    test_pred = calib_fit.predict_proba(test.iloc[index].values.reshape(1, -1))

    #Adding the index back
    df_out = pd.DataFrame(columns=['SK_ID_CURR','TARGET'])
    df_out = df_out.append({'SK_ID_CURR':index,'TARGET':test_pred[:,1][0]}, ignore_index=True)
    return json.dumps({str(df_out.at[0,'SK_ID_CURR']):df_out.at[0,'TARGET']})
