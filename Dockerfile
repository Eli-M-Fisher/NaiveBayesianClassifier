# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "web_server.api_main:app", "--host", "0.0.0.0", "--port", "8000"]
