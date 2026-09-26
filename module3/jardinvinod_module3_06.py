# Import FastAPI
from fastapi import FastAPI, Query

# Import math to calculate total pages
import math


# Create FastAPI application
app = FastAPI()


# Sample data
items = [
    "Item 1", "Item 2", "Item 3", "Item 4", "Item 5",
    "Item 6", "Item 7", "Item 8", "Item 9", "Item 10",
    "Item 11", "Item 12", "Item 13", "Item 14", "Item 15",
    "Item 16", "Item 17", "Item 18", "Item 19", "Item 20"
]


# Create pagination API
@app.get("/items")
def get_items(
    page: int = Query(2, ge=1),
    size: int = Query(5, ge=1)
):

    # Calculate start and end positions
    start = (page - 1) * size
    end = start + size

    # Get items for the requested page
    page_items = items[start:end]

    # Calculate metadata
    total_items = len(items)
    total_pages = math.ceil(total_items / size)

    # Return items and pagination metadata
    return {
        "items": page_items,
        "metadata": {
            "page": page,
            "size": size,
            "total_items": total_items,
            "total_pages": total_pages
        }
    }