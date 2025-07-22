# docker/classifier.Dockerfile

# --- Base image ---
FROM python:3.10-slim

# --- Set working directory inside container ---
WORKDIR /app/classifier_service

# --- Install Python dependencies ---
COPY classifier_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy service code ---
COPY classifier_service/ .

# --- Copy model code from shared /model directory ---
COPY model/ /app/model/

# --- Ensure data directory and copy dataset ---
RUN mkdir -p /app/data
COPY data/phishing.csv /app/data/phishing.csv

RUN echo "Contents of /app/data:" && ls -lah /app/data


# (Optional Debug) Show contents of /app/data during build
# RUN ls -lh /app/data

# --- Set Python path to include the whole app directory ---
ENV PYTHONPATH="${PYTHONPATH}:/app"

# --- Final working directory for uvicorn context ---
WORKDIR /app/classifier_service

# --- Run the FastAPI server ---
CMD ["uvicorn", "classifier_main:app", "--host", "0.0.0.0", "--port", "9000"]
