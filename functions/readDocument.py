import os
import redis
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import request

# Initialize Redis client
redis_client = redis.from_url(os.getenv('REDIS_CONNECTION'), decode_responses=True)

def read_document(doc_id):
    # Get StudentId from query parameters
    student_id = request.args.get('StudentId')

    if not student_id:
        return {"error": "StudentId is required for partition key"}, 400

    # Check if data is available in Redis cache
    redis_key = f"{student_id}:{doc_id}"
    cached_document = redis_client.get(redis_key)
    
    if cached_document:
        document = json.loads(cached_document)
        document["status"] = "Data retrieved from Redis"
        return document

    # Connect to CosmosDB
    connection_string = os.getenv('COSMOS_DB_CONNECTION_STRING')
    db_name = os.getenv('COSMOS_DB_NAME')
    collection_name = os.getenv('COSMOS_DB_COLLECTION')

    mongo_client = MongoClient(connection_string)
    collection = mongo_client[db_name][collection_name]

    # Query CosmosDB with StudentId (Partition Key)
    document = collection.find_one({"_id": ObjectId(doc_id), "StudentId": student_id})

    if document:
        # Convert ObjectId to string
        document['_id'] = str(document['_id'])

        # Cache the result in Redis
        redis_client.set(redis_key, json.dumps(document))

        # Add status field
        document["status"] = "Data retrieved from CosmosDB and cached in Redis"
        return document

    return {"error": "Document not found", "status": "Data not found in Redis or CosmosDB"}, 404
