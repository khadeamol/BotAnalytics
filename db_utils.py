import psycopg2
import os
import numpy as np
np.float_ = np.float64
from elasticsearch import Elasticsearch
import os 
from datetime import datetime, timezone

DB_URL = os.getenv("DATABASE_URL")

es = Elasticsearch([os.getenv("ELASTICSEARCH_URL","http://localhost:9200")])

# Test the connection
if es.ping():
    print("Connected to Elasticsearch!")
else:
    print("Elasticsearch connection failed.")

index_name = "chat_history"

# Define mapping (structure of data)
mapping = {
    "mappings": {
        "properties": {
            "user_message": {"type": "text"},
            "bot_response": {"type": "text"},
            "timestamp": {"type": "date"}
        }
    }
}

# Create the index if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created successfully.")
else:
    print(f"Index '{index_name}' already exists.")

def store_chat(user_message, bot_response):
    es.index(index="chat_messages", body={
        "user_message": user_message,
        "bot_response": bot_response,
        "timestamp": datetime.now(timezone.utc)
    })
    print("Chat stored in Elasticsearch.")
