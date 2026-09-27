# Use Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI program
COPY jardinvinod_module7_03.py .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI server
# 0.0.0.0 is important so the API can be reached outside the container
CMD ["uvicorn", "jardinvinod_module7_03:app", "--host", "0.0.0.0", "--port", "8000"]