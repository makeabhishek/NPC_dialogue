# npc_server.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
import requests
import tiktoken

app = FastAPI()

conversation_history: List[Dict] = []
token_limit = 4000

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

class Message(BaseModel):
    role: str
    content: str

@app.post("/add_message")
def add_message(msg: Message):
    conversation_history.append(msg.dict())
    return {"status": "added"}

@app.get("/get_context")
def get_context():
    token_count = 0
    recent_context = []
    for message in reversed(conversation_history):
        tokens = len(encoding.encode(message["content"]))
        if token_count + tokens > token_limit:
            break
        recent_context.insert(0, message)
        token_count += tokens
    return {"context": recent_context}

@app.post("/summarize_history")
def summarize_history():
    if len(conversation_history) <= 5:
        return {"summary": "Not enough history to summarize."}
    summary = "Summary of past events: " + " ".join([m["content"] for m in conversation_history[:-5]])
    conversation_history.clear()
    conversation_history.append({"role": "system", "content": summary})
    return {"summary": summary}

@app.post("/reset")
def reset():
    conversation_history.clear()
    return {"status": "cleared"}

@app.get("/tool_call")
def tool_call(query: str):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query.replace(' ', '_')}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {"result": data.get("extract", "No summary available.")}
    return {"result": "Failed to fetch from Wikipedia."}
