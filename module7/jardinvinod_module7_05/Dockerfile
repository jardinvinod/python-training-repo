# Use Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy Python program
COPY jardinvinod_module7_05.py .

# Create directory where persistent database will be mounted
RUN mkdir -p /data

# Run application
CMD ["python", "jardinvinod_module7_05.py"]