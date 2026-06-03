from openai import OpenAI
from dotenv import load_dotenv


def load_api_client():
    load_dotenv()
    client = OpenAI()
    return client


def get_prompt_user(client, prompt):
    response = client.responses.create(
        model="gpt-5-nano",
        input= prompt,
        store=False,
    )
    print("AI:", response.output_text)
    
def create_prompt_without_cot():
        prompt = [{
                "role": "system",
								"content": ("""	Solve step by step internally, but return only the final answer:

    A shop sells a pen for ₹10.
    If you buy 7 pens and pay ₹100,
    how much change will you get?""")
				}                                                                  
        ]
                   
        return prompt  
def create_prompt_with_cot():  
        prompt = [{
                "role": "system",
								"content": ("""	Show it  step by step :

    A shop sells a pen for ₹10.
    If you buy 7 pens and pay ₹100,
    how much change will you get?""")
				}                                                                  
        ]
        return prompt 
        
    
				
try:
    client = load_api_client()
    prompt1 = create_prompt_without_cot()
    prompt2 = create_prompt_with_cot()

    user_prompt = get_prompt_user(client, prompt1)
    user_prompt = get_prompt_user(client, prompt2)

except Exception as ex:
    print("Error:", ex)