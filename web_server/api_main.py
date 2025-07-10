from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from core.controller import Controller
import os

app = FastAPI()

# Define the target column and dataset path
FILE_PATH = "data/phishing.csv"
TARGET_COLUMN = "class"

# Load trained model once
controller = Controller(FILE_PATH, TARGET_COLUMN)
controller.load_data()
controller.train()

# Serve static HTML
app.mount("/static", StaticFiles(directory="web_server/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_form():
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
    try:
        prediction = controller.predict_single(input_data.features)
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))