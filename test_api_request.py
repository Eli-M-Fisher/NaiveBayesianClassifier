import requests
import json

# Load input from JSON file
with open("sample_input.json", "r") as file:
    input_data = json.load(file)

# Send POST request to FastAPI server
response = requests.post("http://127.0.0.1:8000/predict", json=input_data)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())