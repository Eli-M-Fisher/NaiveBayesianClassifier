# Base step
FROM python:3.10-slim

# Setting the working folder
WORKDIR /app

# Copying requirements
COPY requirements.txt .

# Installing the libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Opening port 8000
EXPOSE 8000

# Running the FastAPI server
CMD ["uvicorn", "web_server.api_main:app", "--host", "0.0.0.0", "--port", "8000"]