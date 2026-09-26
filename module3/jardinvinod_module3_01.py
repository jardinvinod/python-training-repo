# Import FastAPI
from fastapi import FastAPI


# Create FastAPI application
app = FastAPI()


# Create /hello endpoint
@app.get("/hello")
def say_hello(name: str):

    # Return greeting message
    return {
        "message": f"Hello {name}"
    }
    