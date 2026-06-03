from openai import OpenAI
from dotenv import load_dotenv

import os

def load_api_client():
		load_dotenv()
		client = OpenAI()
		return client

def create_prompt(prompt	):
    SYSTEM_PROMPT = """
        You are an mood analyzer. 
        You judge the mood of the user based on the input text.  
        Example1:
          User: I got new job.
          AI: The user is feeling happy.
				Example2:
          User: I am listening to music.
					AI: The user is feeling happy.
        Example3:
         User : I lost my mobile phone.
				 AI: The user is feeling sad.
        Example4:
				 User : I am stuck in traffic jam.
        AI: The user is feeling frustrated.    
		"""
          
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