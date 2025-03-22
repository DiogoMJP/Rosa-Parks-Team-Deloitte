from dotenv import load_dotenv

from app import update_max_tokens, update_temperature
load_dotenv(override=True)

import faiss
from openai import AzureOpenAI
from src.services.models.embeddings import Embeddings
from src.services.vectorial_db.faiss_index import FAISSIndex
from src.services.models.llm import LLM
import os
import time

def rag_chatbot(llm: LLM, input_text: str, history: list, index: FAISSIndex, temp: temperature):
    """Retrieves relevant information from the FAISS index, generates a response using the LLM, and manages the conversation history.

    Args:
        llm (LLM): An instance of the LLM class for generating responses.
        input_text (str): The user's input text.
        history (list): A list of previous messages in the conversation history.
        index (FAISSIndex): An instance of the FAISSIndex class for retrieving relevant information.

    Returns:
        tuple: A tuple containing the AI's response and the updated conversation history.
    """

    # Retrieve context from the FAISS Index
    def retrieve_context(query, k=3):
        context = index.retrieve_chunks(query, k)  
        return context

    # Generate a response using the LLM
    def generate_response(query, context, history):
        context_str = "\n".join(context)  
        temperature = update_temperature()
        tokens = update_max_tokens()
        # Get the response and updated history from the LLM
        response, updated_history = llm.get_response(history, context_str, query, temperature, tokens)  
        
        return response, updated_history

    context = retrieve_context(input_text)
    ai_response, history = generate_response(input_text, context, history)

    return ai_response, history


def main():
    """Main function to run the chatbot."""

    embeddings = Embeddings()
    
    # Initialize the FAISS index with the embeddings function
    index = FAISSIndex(embeddings=embeddings.get_embeddings)

    try:
        index.load_index()  # Try to load the FAISS index from disk
    except FileNotFoundError:
        raise ValueError("Index not found. You must ingest documents first.")

    llm = LLM()  # Initialize the LLM (assumed to be a wrapper for the Azure OpenAI API)
    history = []  # Start with an empty conversation history
    print("\n# INITIALIZED CHATBOT #")

    while True:
        user_input = str(input("You:  "))  # Get user input
        if user_input.lower() == "exit":  # Exit the loop if user types 'exit'
            break
        
        response, history = rag_chatbot(llm, user_input, history, index)  # Get AI response and updated history
        print("AI: ", response)

if __name__ == "__main__":
    main()
