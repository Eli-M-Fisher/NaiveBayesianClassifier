# Naive Bayesian Classifier

This is a simple machine learning web application that uses a Naive Bayes classifier to detect phishing websites based on a CSV dataset.  
The app is split into two Docker services, one for the API and one for the classification logic, and is fully containerized for portability and ease of deployment.

## Features

- Upload and train on a CSV file (default: `phishing.csv`)
- Predict whether a website is phishing or legitimate
- Clean and preprocess data automatically
- Logging to `logs/app.log` inside the containers
- Modular and easy to maintain
- Simple HTML frontend for interacting with the API

## Technologies Used

- **Python 3**
- **FastAPI** for the API
- **scikit-learn** for the Naive Bayes model
- **Pandas / NumPy** for data handling
- **Docker** for containerization
- **Docker Compose** to orchestrate services

## Architecture

The app is split into two services:

1. **API Service (FastAPI)**  
   Handles all incoming requests from users (like a receptionist). It routes the data to the classifier service and returns the response. It also serves a static HTML form.

2. **Classifier Service**  
   Loads and trains the Naive Bayes model. This service is responsible for the actual classification logic — either by loading a previously trained model (`model/trained_model.pkl`) or training a new one from scratch if the model file is missing.

Each service runs in its own Docker container, communicating via an internal Docker network.


## How to Run

1. Clone the repo:
   ```bash
   git clone https://github.com/yourname/NaiveBayesianClassifier.git
   cd NaiveBayesianClassifier
   
2. Build and start the services:

```docker-compose up --build```

3. Open your browser and visit:
http://localhost:8000

4. Fill in the form and submit to see predictions.

## Training & Prediction
- The model is trained on startup from data/phishing.csv, unless a trained model already exists in model/trained_model.pkl.

- The API receives feature values from the user via the form (or JSON) and returns a binary classification: 1 for phishing, -1 for legitimate.

## Folder Structure
```
NaiveBayesianClassifier/
├── core/
│   ├── controller.py          # Handles data loading, cleaning, model training
│   ├── naive_bayes.py         # Contains model logic
│   └── logger.py              # Central logging configuration
│
├── web_server/
│   └── static/
│       └── form.html          # Simple HTML UI
│
├── model/
│   └── trained_model.pkl      # Saved model
│
├── data/
│   └── phishing.csv           # Default training dataset
│
├── logs/
│   └── app.log                # Log file for both services
│
├── docker/
│   ├── api.Dockerfile         # Builds API container
│   └── classifier.Dockerfile  # Builds classifier container
│
├── docker-compose.yml         # Defines services and their interaction
├── api_main.py                # FastAPI server entrypoint
├── classifier_main.py         # Classifier server entrypoint
└── requirements.txt           # Python dependencies
```

## Logs
Each container writes to logs/app.log inside its own environment.
You can read logs using:

```docker exec -it classifier_service cat /app/logs/app.log
docker exec -it api_service cat /app/logs/app.log
```

## Future Plans
- Add support for uploading arbitrary CSV datasets via the browser

- Add version control for different models

- Add real-time model retraining from user input

Add authentication and analytics dashboard

## Current Versions
- v0/no-docker: Pure Python version without Docker

- v1/docker-initial: First Docker version (single container)

- v2/docker-services: Split API and classifier into two separate services
