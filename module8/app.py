from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from database import (
    add_information,
    get_all_information,
    get_information_by_id,
    search_information,
    delete_information
)


app = FastAPI(
    title="LLM Database Application",
    description="FastAPI application using SQLite, MCP and Ollama",
    version="1.0"
)


# ---------------------------------------------------------
# PYDANTIC MODELS
# ---------------------------------------------------------

class InformationInput(BaseModel):
    name: str
    category: str
    information: str


class SearchInput(BaseModel):
    search_text: str


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "LLM Database Application is running",
        "docs": "/docs"
    }


# ---------------------------------------------------------
# ADD INFORMATION
# ---------------------------------------------------------

@app.post("/information")
def create_information(data: InformationInput):

    record_id = add_information(
        name=data.name,
        category=data.category,
        information=data.information
    )

    return {
        "message": "Information stored successfully",
        "id": record_id,
        "data": data
    }


# ---------------------------------------------------------
# GET ALL INFORMATION
# ---------------------------------------------------------

@app.get("/information")
def read_all_information():

    return get_all_information()


# ---------------------------------------------------------
# GET INFORMATION BY ID
# ---------------------------------------------------------

@app.get("/information/{record_id}")
def read_information(record_id: int):

    record = get_information_by_id(record_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Information not found"
        )

    return record


# ---------------------------------------------------------
# SEARCH DATABASE
# ---------------------------------------------------------

@app.post("/search")
def search_database(data: SearchInput):

    results = search_information(data.search_text)

    return {
        "search": data.search_text,
        "results": results
    }


# ---------------------------------------------------------
# DATABASE CONTEXT FOR MCP / LLM
# ---------------------------------------------------------

@app.get("/context")
def database_context():
    """
    Return all database records.

    The MCP server uses this endpoint to obtain context
    before sending a question to the LLM.
    """

    records = get_all_information()

    return {
        "records": records
    }


# ---------------------------------------------------------
# DELETE INFORMATION
# ---------------------------------------------------------

@app.delete("/information/{record_id}")
def remove_information(record_id: int):

    success = delete_information(record_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Information not found"
        )

    return {
        "message": "Information deleted successfully"
    }