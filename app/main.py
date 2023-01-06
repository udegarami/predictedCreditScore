from typing import List
from fastapi import FastAPI
from models import User, Query, Prediction

app = FastAPI()

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

#Import CSV as a DB
import csv

client_list = []

with open('xgboost_calibrated.csv', newline='') as csv_file:
    reader = csv.reader(csv_file)
    next(reader, None)  # Skip the header.
    # Unpack the row directly in the head of the for loop.
    for id, score in reader:
        # Convert the numbers to floats.
        score = float(score)
        # Now create the Student instance and append it to the list.
        client_list.append(Prediction(id, score))

@app.get("/")
async def root():
    #await request()
    return {"Hello": "World"}

@app.get("/api/v1/users")
async def fetch_users():
    return db;

@app.post("/api/v1/queryFav")
async def saveQueryFav(query: Query):
    query.append(query)
    return{id: query.id}