from openai import OpenAI
from dotenv import load_dotenv

import os

def load_api_client():
		load_dotenv()
		client = OpenAI()
		return client

def create_prompt(prompt	):
    SYSTEM_PROMPT = (
        "You are an English assistant. "
        "You accept incorrect grammar and spelling mistakes. "
        "You correct the grammar and spelling mistakes and provide the corrected version of the text. "
        "Example: If the user input is 'I has a cat', you should respond with 'I have a cat'. "
    )
    return SYSTEM_PROMPT 

def get_prompt_user(client, system_prompt, user_text):
    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ],
        store=False,
    )
    print("AI:", response.output_text)
    
try:
    client = load_api_client()
    while True:
        question = input("type your sentence? ")
        if question.lower() == 'exit':
            print("Bot : Goodbye!!!")
            break
        prompt = create_prompt(question)
        user_prompt = get_prompt_user(client, prompt, question)
        

except Exception as ex:
    print("Error:", ex)