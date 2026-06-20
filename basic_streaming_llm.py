import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

key = os.getenv("GROQ_API_KEY")

client = OpenAI(api_key=key, base_url="https://api.groq.com/openai/v1")

response = client.chat.completions.create(
    model= "meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
            {"role": "system", "content": "you are a story teller."},
            {"role": "user", "content": "write 1000 words story"}
        ],
    stream=True
)

for chunk in response:
    delta = chunk.choices[0].delta.content
    if delta:
        print(delta, end="", flush=True)