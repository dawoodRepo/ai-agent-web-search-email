# AI Agent with Web Search & Email Tools

An LLM-powered agent that can autonomously search the web and send emails based on natural language prompts — demonstrating function/tool calling and agentic loops.

## Demo
[Add a screenshot or terminal output GIF here]

## Problem
LLMs can't take real-world actions on their own. This project gives an LLM access to external tools (web search, email) and lets it decide when and how to use them to complete a task.

## How it works
1. User provides a natural language prompt (e.g. "search for today's AI news and email it to X")
2. The LLM (via Groq) evaluates whether it needs a tool, returning either a direct answer or a tool call request
3. If a tool call is requested, the corresponding function runs:
   - `search(query)` — searches the web via the Tavily API
   - `send_email(to, subject, body)` — sends an email via the Gmail API
4. Tool output is fed back into the conversation, and the loop continues until the LLM produces a final response

`basic_streaming_llm.py` is a smaller standalone script showing a simple streaming chat completion via Groq, included as a stepping stone toward the full agent.

## Tech Stack
- Python
- Groq API (LLM inference, LLaMA 4 Scout)
- Tavily API (web search)
- Gmail API with OAuth2 (email sending)

## Key Features
- Full agentic tool-calling loop
- Real-time web search integration
- Programmatic email sending via OAuth2-authenticated Gmail

## Setup
```bash
pip install -r requirements.txt
```
Create a `.env` file with:
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key

Run `gmail_auth.py` once to generate your own `token.json` using your Google OAuth credentials (`credentials.json`, obtained from Google Cloud Console). Neither file is included in this repo for security reasons.

## What I learned
Implementing the tool-calling loop manually (checking `finish_reason` and routing to the right function) gave me a clear understanding of how agent frameworks like LangChain's agents work under the hood.