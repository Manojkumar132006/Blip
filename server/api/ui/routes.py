import os
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pymongo import MongoClient

router = APIRouter()

# MongoDB Configuration from Environment Variables
MONGO_URI = os.environ.get("MONGO_URI")
DATABASE_NAME = os.environ.get("DATABASE_NAME")

if not MONGO_URI or not DATABASE_NAME:
    raise ValueError("MONGO_URI and DATABASE_NAME must be set as environment variables")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]


@router.get("/ui/{collection_path:path}/{document_name}")
async def get_ui(collection_path: str, document_name: str):
    """
    Serves UI configuration from MongoDB based on the collection path and document name.
    """
    collection_name = collection_path.replace("/", ".")
    collection = db[collection_name]

    # Fetch data from MongoDB
    try:
        document = collection.find_one({"_id": document_name})
        if document:
            # Remove the "_id" field, which is not JSON serializable by default
            document.pop("_id", None)
            return JSONResponse(content=document)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document '{document_name}' not found in collection '{collection_name}'",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching UI configuration: {str(e)}",
        )
