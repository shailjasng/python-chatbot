from genericpath import exists
import json
from openai import OpenAI
from dotenv import load_dotenv

import os

def load_api_client():
    load_dotenv()
    client = OpenAI()
    return client

def save_chat_history(messages):
    with open("chat_history.json", "w") as f:
        json.dump(messages, f, indent=4)
        
def load_chat_history():
    if exists("chat_history.json"):
        with open("chat_history.json", "r") as f:
            return json.load(f),False
    else:
        messages = [
            {"role": "system", 
             "content": (
                 "You are a helpful assistant. "
                 "Accept only questions related to programming and technology. "
                 "If the question is not related to programming or technology, politely decline to answer."
                        )},
        ]
        return messages,True


def chat_with_ai(client, messages):
    response = client.responses.create(
        model="gpt-5-nano",
        input=messages,
        store=False, 
        stream=True
    )
    # in case of streaming response, we need to concatenate the chunks to get the final response text
    final_text = ''
    for event in response:
        if event.type == "response.output_text.delta":
            print(event.delta, end="")
            final_text += event.delta
    
    print()
    return final_text
         

# print(response.output_text)
# return response.output_text
try:
    client = load_api_client()
    messages, is_new_chat = load_chat_history()
    if is_new_chat:
        print("Hello there, how can I help you? I am a programming assistant, ask me anything related to programming and technology.")
    while True:
        question = input("type your question? ")
        if question.lower() == 'exit':
            print("Bot : Goodbye!!!")
            break

        messages.append({"role": "user", "content": question})
        response_text = chat_with_ai(client, messages)
        if response_text.strip():
          messages.append({"role": "assistant", "content": response_text})
          save_chat_history(messages)
except Exception as ex:
    print("Error:", ex)
  
  
  
