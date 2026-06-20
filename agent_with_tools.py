# from groq import Groq
# from dotenv import load_dotenv
# import os

# load_dotenv()

# client = Groq()

# messages = [
#     {"role": "system", "content": "You are a helpful assistant."}
# ]

# while True:
#     user_message = input("You:")

#     messages.append({"role": "user", "content": user_message})

#     response = client.chat.completions.create(
#         model="llama-3.3-70b-versatile",  # free & very capable
#         messages=messages
#     )

#     messages.append({"role": "assistant", "content": response.choices[0].message.content})
#     print("AI:", response.choices[0].message.content)

# for gmail
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from dotenv import load_dotenv
import os
from tavily import TavilyClient
import requests
import json

load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")

client = TavilyClient(api_key=tavily_api_key)

# search function
def search(query="latest ai news"):
    print("searching web...")
    # result = client.search(query)
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": tavily_api_key,
            "query": query
        }
    )
    return response.json()


# gmail sending function
def send_email(to, subject, body):
    print("sending email...")
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/gmail.send'])
    service = build('gmail', 'v1', credentials=creds)
    
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service.users().messages().send(userId='me', body={'raw': raw}).execute()
    
    return "Email sent successfully!"


# LLM
messages = [
    {"role":"system", "content": "You are a helpful assistant that can search the web and send emails. IMPORTANT: Never call the same tool twice. After a tool returns a result, use that result to respond to the user. if subject is not provided for email, then add it yourself"}
]

tools = [
    {
        "type": "function",
        "function": {
            "name": "search",
            "description": "Search the internet for current information on a given query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up on the internet."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "send_email",
        "description": "Send an email to a given address with a subject and body.",
        "parameters": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "The recipient's email address."
                },
                "subject": {
                    "type": "string",
                    "description": "The subject of the email."
                },
                "body": {
                    "type": "string",
                    "description": "The body content of the email."
                }
            },
            "required": ["to", "subject", "body"]
            }
        }
    }
]

functions = {
    "search": search,
    "send_email": send_email
}

grok_api_key = os.getenv("GROQ_API_KEY")

user_prompt = input("enter your prompt: ")
messages.append({"role": "user", "content": user_prompt})

while True:
    response = requests.post("https://api.groq.com/openai/v1/chat/completions",
                            headers={
                                "Authorization": f"Bearer {grok_api_key}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "model": "meta-llama/llama-4-scout-17b-16e-instruct",
                                "messages": messages,
                                "tools": tools
                            }
                            )

    # print(response.json())
    data = response.json()
    finish_reason = data['choices'][0]['finish_reason']

    if finish_reason == 'tool_calls':
        tool_call = data['choices'][0]['message']['tool_calls'][0]
        function_name = tool_call['function']['name']
        arguments = json.loads(tool_call['function']['arguments'])

        my_function = functions[function_name]
        result = my_function(**arguments)

        messages.append({'role':'assistant', 'content':None, 'tool_calls':[tool_call]})
        messages.append({
            'role':'tool',
            'tool_call_id':tool_call['id'],
            'content':json.dumps(result),
        })


    elif finish_reason == 'stop':
        print(data['choices'][0]['message']['content'])
        break