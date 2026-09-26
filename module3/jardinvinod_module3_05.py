# Import FastAPI
from fastapi import FastAPI

# Import logging module
import logging


# Create FastAPI application
app = FastAPI()


# Create logger
logger = logging.getLogger("request_logger")

# Set logging level
logger.setLevel(logging.INFO)


# Create console handler
console_handler = logging.StreamHandler()

# Create file handler
file_handler = logging.FileHandler("my_file.log")


# Define log format
log_format = logging.Formatter(
    "%(asctime)s - %(message)s"
)

# Apply format to both handlers
console_handler.setFormatter(log_format)
file_handler.setFormatter(log_format)


# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)


# Middleware to log every request
@app.middleware("http")
async def log_requests(request, call_next):

    # Process the request
    response = await call_next(request)

    # Get request method
    method = request.method

    # Get request path
    path = request.url.path

    # Get response status code
    status = response.status_code

    # Create log message
    logger.info(
        f"Method: {method} | Path: {path} | Status: {status}"
    )

    # Return response
    return response


# Test endpoint
@app.get("/")
def home():
    return {
        "message": "Logging API is running"
    }


# Another test endpoint
@app.get("/hello")
def hello():
    return {
        "message": "Hello"
    }