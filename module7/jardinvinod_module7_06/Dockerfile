# Use Python base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy Streamlit Python program
COPY jardinvinod_module7_06.py .

# Streamlit port
EXPOSE 8501

# Default environment variable
ENV USE_PERSONA=false

# Start Streamlit
CMD ["streamlit", "run", "jardinvinod_module7_06.py", "--server.address=0.0.0.0", "--server.port=8501"]