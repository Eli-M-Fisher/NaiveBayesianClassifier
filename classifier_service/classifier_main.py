from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from model.naive_bayes import NaiveBayesClassifier
from core.cleaner import Cleaner
import os
import pandas as pd
import joblib
from core.logger import logger
from fastapi.responses import JSONResponse

app = FastAPI()
model = NaiveBayesClassifier()

MODEL_PATH = "model/trained_model.pkl"
CSV_PATH = "/app/data/phishing.csv"

@app.on_event("startup")
def load_or_train_model():
    if os.path.exists(MODEL_PATH):
        logger.info("[CLASSIFIER] Loading model from file...")
        model.load(MODEL_PATH)
    else:
        logger.info("[CLASSIFIER] No trained model found. Training from phishing.csv...")
        df = pd.read_csv(CSV_PATH)

        identifier_columns = ['Index'] if 'Index' in df.columns else []
        cleaner = Cleaner(df)
        df_cleaned = cleaner.clean(identifier_columns)

        model.train(df_cleaned)
        model.save(MODEL_PATH)
        logger.info("[CLASSIFIER] Model trained and saved.")

class RecordInput(BaseModel):
    features: dict

@app.post("/predict")
def predict(input_data: RecordInput):
    try:
        logger.info("POST /predict called with input: %s", input_data.features)
        prediction = model.classify_record(input_data.features)
        logger.info("Prediction result: %s", prediction)
        return {"prediction": prediction}
    except Exception as e:
        logger.error("Prediction failed: %s", str(e))
        raise HTTPException(status_code=500, detail="Prediction error")

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})
