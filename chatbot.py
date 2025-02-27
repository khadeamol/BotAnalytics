import ollama
import os 

class Chatbot():
    def __init__(self, model_name = "llama3.2:1b"):
        """Initializing the chatbot with llama"""
        self.model_name = model_name

    def get_response(self, message):
        response = ollama.chat(model=self.model_name, messages=[{"role":"user", "content":message}],         options={
            "num_predict": 1000,   # Limits max tokens in response (default is too high)
            "temperature": 0.2,   # Lower = more deterministic, slightly faster
            "top_k": 40,          # Restrict next token choices
            "top_p": 0.9          # Reduce probability range
        })
        # store_chat(query.user_id, query.message, response)
        return response["message"]["content"]

        