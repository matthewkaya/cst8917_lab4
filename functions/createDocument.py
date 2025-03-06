import os
from pymongo import MongoClient

def create_document(data):
    # Ortam değişkeninden bağlantı bilgisini al
    connection_string = os.getenv('COSMOS_DB_CONNECTION_STRING')
    db_name = os.getenv('COSMOS_DB_NAME')
    collection_name = os.getenv('COSMOS_DB_COLLECTION')

    if not connection_string:
        return {"error": "COSMOS_DB_CONNECTION_STRING is missing"}, 500

    client = MongoClient(connection_string)
    collection = client[db_name][collection_name]

    # StudentId'nin olup olmadığını kontrol et
    if "StudentId" not in data:
        return {"error": "Missing StudentId (Partition Key)"}, 400

    result = collection.insert_one(data)

    return {"status": "success", "id": str(result.inserted_id)}
