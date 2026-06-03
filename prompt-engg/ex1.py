from openai import OpenAI
from dotenv import load_dotenv


def load_api_client():
		load_dotenv()
		client = OpenAI()
		return client

def solve_without_cot():
    response = client.responses.create(
        model="gpt-5-nano",
        input=prompt,
        store=False, 
    )
    return response.output_text
def create_prompt(topic):
        prompt = [
                        {
                "role": "system",
                "content": (	"You are a helpful assistant. "
                "Accept only questions related to programming and technology. "
                "If the question is not related to programming or technology, politely decline to answer.")
                
                                                },
       {
                "role": "user",
                "content": f"hello explain {topic} in bullet points in simple terms along with an example?"
             }                                                                             
        ]
            
        
        return prompt

try:
    client = load_api_client()
    question = input("type your question? ")
    prompt = create_prompt(question)
    user_prompt = get_prompt_user(client, prompt)
    print(user_prompt)

except Exception as ex:
    print("Error:", ex)