import os
from pymongo import MongoClient


def create_document(data):
    # Retrieve environment variables
    connection_string = os.getenv('COSMOS_DB_CONNECTION_STRING')
    db_name = os.getenv('COSMOS_DB_NAME')
    collection_name = os.getenv('COSMOS_DB_COLLECTION')

    if not connection_string:
        return {"error": "COSMOS_DB_CONNECTION_STRING is missing", "status": "failed"}, 500

    # Check if StudentId (Partition Key) is provided
    if "StudentId" not in data:
        return {"error": "Missing StudentId (Partition Key)", "status": "failed"}, 400

    try:
        # Secure connection to Cosmos DB with TLS settings
        client = MongoClient(connection_string, tls=True, tlsAllowInvalidCertificates=False, serverSelectionTimeoutMS=5000)
        collection = client[db_name][collection_name]

        result = collection.insert_one(data)

        return {"status": "success", "id": str(result.inserted_id)}
    except Exception as e:
        return {"error": str(e), "status": "failed"}, 500
