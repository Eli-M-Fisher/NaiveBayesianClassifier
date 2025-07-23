# # Base step
# FROM python:3.10-slim
#
# # Setting the working folder
# WORKDIR /app
#
# # Copying requirements
# COPY requirements.txt .
#
# # Installing the libraries
# RUN pip install --no-cache-dir -r requirements.txt
#
# # Copy the app code
# COPY . .
#
# # Opening port 8000
# EXPOSE 8000
#
# # Running the FastAPI server
# CMD ["uvicorn", "web_server.api_main:app", "--host", "0.0.0.0", "--port", "8000"]

# Base step
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy base requirements
COPY requirements.txt .

# Install base requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Expose API port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "web_server.api_main:app", "--host", "0.0.0.0", "--port", "8000"]
