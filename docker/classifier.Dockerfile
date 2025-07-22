# Base step: Official Python
FROM python:3.10-slim

# Setting the working directory inside the container
WORKDIR /app

# Copying and installing requirements
COPY classifier_service/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the service code
COPY classifier_service/ .

# Copy the model module from the main project
COPY model/ model/

# Run command
CMD ["uvicorn", "classifier_main:app", "--host", "0.0.0.0", "--port", "8001"]