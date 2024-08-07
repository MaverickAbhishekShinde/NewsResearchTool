import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()
api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
model = "gpt-4"

client = AzureOpenAI(api_key=api_key, api_version="2023-03-15-preview", azure_endpoint=endpoint)

def ask_question(question):
    conversation = [{"role": "user", "content": question}, {"role": "system", "content": "I can answer your questions or follow your instructions."}]
    response = client.chat.completions.create(model=model, messages=conversation)
    return response.choices[0].message.content

# Example usage:
# question = "Why is Chennai weather so hot?"
# answer = ask_question(question)
# print("Answer:", answer)

while(True):
    question = str(input("Enter Query: "))
    print((ask_question(question)))