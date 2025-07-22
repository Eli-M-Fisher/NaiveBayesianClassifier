from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from core.logger import logger
import requests
import os

app = FastAPI()

# Define classifier service URL
CLASSIFIER_URL = os.getenv("CLASSIFIER_URL", "http://localhost:9000")

# Serve static HTML
app.mount("/static", StaticFiles(directory="web_server/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_form():
    logger.info("GET / called")
    file_path = "web_server/static/form.html"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Form HTML not found")
    with open(file_path, "r") as f:
        return f.read()

# Define input schema for API using Pydantic
class RecordInput(BaseModel):
    features: dict

@app.post("/predict")
def predict(input_data: RecordInput):
    logger.info("POST /predict called with input: %s", input_data.features)

    try:
        response = requests.post(
            f"{CLASSIFIER_URL}/predict",
            json={"features": input_data.features},
            timeout=5
        )
        response.raise_for_status()
        prediction = response.json().get("prediction")
        logger.info("Prediction response from classifier service: %s", prediction)
        return {"prediction": prediction}
    except requests.RequestException as e:
        logger.error("Failed to get prediction from classifier service: %s", str(e))
        raise HTTPException(status_code=500, detail="Classifier service error")
