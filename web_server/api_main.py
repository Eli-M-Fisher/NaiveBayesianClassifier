from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core.controller import Controller

app = FastAPI()

# Define the target column for classification
FILE_PATH = "data/phishing.csv"
TARGET_COLUMN = "class"

# Load the trained controller once
controller = Controller(FILE_PATH, TARGET_COLUMN)
controller.load_data()
controller.train()

# Define input schema for API using Pydantic
class RecordInput(BaseModel):
    features: dict

@app.get("/")
def read_root():
    return {"message": "Naive Bayes Classifier API is running."}

@app.post("/predict")
def predict(input_data: RecordInput):
    try:
        prediction = controller.predict_single(input_data.features)
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))