from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from core.controller import Controller
from core.logger import logger
import os

app = FastAPI()

# Define the target column and dataset path
FILE_PATH = "data/phishing.csv"
TARGET_COLUMN = "class"

# Load trained model once with error handling
controller = None
try:
    logger.info("Initializing Controller for API...")
    controller = Controller(FILE_PATH, TARGET_COLUMN)
    controller.load_data()
    controller.train()
    logger.info("API controller loaded and model trained.")
except Exception as e:
    logger.error("Failed to initialize controller: %s", str(e))
    controller = None  # Optional: keep None to handle gracefully later

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

    if controller is None:
        logger.error("Controller not initialized")
        raise HTTPException(status_code=500, detail="Model not available")

    try:
        prediction = controller.predict_single(input_data.features)
        logger.info("Prediction response: %s", prediction)
        return {"prediction": prediction}
    except Exception as e:
        logger.error("Prediction failed: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
