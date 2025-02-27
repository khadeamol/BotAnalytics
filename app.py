from fastapi import FastAPI
# , Depends
from pydantic import BaseModel
from chatbot import Chatbot
from retriever import retrieve_context
from db_utils import store_chat

app = FastAPI()

chatbot = Chatbot()


class Query(BaseModel):
    message: str

@app.post("/chat/")
async def chat(query: Query):
    """Handles user messages and returns response"""
    context = retrieve_context(query.message) # Retrieve relevant data from ElasticSearch
    print("Context is:", context)
    response = chatbot.get_response(query.message)
    store_chat(query.message, response)
    return {"response": response}