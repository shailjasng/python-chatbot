from google import genai
from google.genai import types
from dotenv import load_dotenv


def get_gemini_client():
		load_dotenv()
		return genai.Client()

def chat_with_gemini(client, content_list):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=content_list,
        config=types.GenerateContentConfig(
            system_instruction="You are a helpful assistant.",            
        )        
    )
    return response.text

try:
    client = get_gemini_client()
    content_list = []

    while True:
        question = input("type your question? ")
        if question.lower() == 'exit':
            print("Bot : Goodbye!!!")
            break

        content_list.append(types.Content(role="user", parts= [types.Part(text=question)]))
        response_text = chat_with_gemini(client, content_list)
        print("Bot :", response_text)
        content_list.append(types.Content(role="model", parts= [types.Part(text=response_text)]))
except Exception as ex:
   print("Error:", ex)

