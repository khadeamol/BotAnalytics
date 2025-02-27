import numpy as np
np.float_ = np.float64
from elasticsearch import Elasticsearch
import os 

es = Elasticsearch([os.getenv("ELASTICSEARCH_URL","http://localhost:9200")])

# Test the connection
if es.ping():
    print("Connected to Elasticsearch!")
else:
    print("Elasticsearch connection failed.")

index_name = "chat_messages"

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

# Create index
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created.")


def retrieve_context(query):
    search_body = {"query":{"match":{"content":query}}}
    response = es.search(index = "chat_history", body = search_body)
    if response["hits"]["hits"]:
        return response["hits"]["hits"][0]["_source"]["content"]
    return ""