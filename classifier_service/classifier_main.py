from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from model.naive_bayes import NaiveBayesClassifier
import pandas as pd
import os
import joblib

app = FastAPI()
classifier = NaiveBayesClassifier()

MODEL_PATH = "trained_model.pkl"

class PredictInput(BaseModel):
    features: dict

@app.on_event("startup")
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError("Model file not found.")
    classifier.load(MODEL_PATH)

@app.post("/predict")
def predict(input_data: PredictInput):
    try:
        df = pd.DataFrame([input_data.features])
        prediction = classifier.predict(df)
        return {"prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
