# NPC Dialogue System Using Model Context Protocol (MCP)

## Adam the Sage — NPC Dialogue System

This project builds a dialogue engine for an NPC (Non-Player Character) named **Adam** using a custom **Model Context Protocol (MCP)**, LangGraph for dialogue routing, and GPT-based conversations.

Adam is a centuries-old, wise sage from the northern isles who speaks with empathy and shares ancient lore.

---

## Project Structure
/your_project/ ├── mcp_server.py # MCP Server - handles context, memory, and tool use ├── mcp_client.py # MCP Client - chat interface with LangGraph workflow ├── .env # Secret API keys ├── requirements.txt # Required Python libraries ├── README.md # Setup instructions and description

---

## Setup Instructions
To Set This Up Locally

### 1. Clone / Download Project
Clone this repo or download the files into a folder.

### 2. Create `.env` File for API KEYS
Create a `.env` file in your project folder with this content:

```env
OPENAI_API_KEY="your-openai-api-key-here"
LANGCHAIN_API_KEY="your-langchain-api-key-here"
LANGCHAIN_PROJECT="GenAIAPP" 
```

- Replace `your-openai-api-key-here` with your actual OpenAI key.
- Replace `your-langchain-api-key-here` with your actual LANGCHAIN key.
- The client (`mcp_client.py`) reads your key automatically using `python-dotenv`.

## 3. Install Dependencies
### Virtual environemnt 
Create virtual environemnt (-y for default packages installation)
```python
conda create -p venv python==3.10 -y
conda activate venv
```

Install all required Python libraries using:
```bash
pip install -r requirements.txt
```
### Requirements file
`requirements.txt` contents:
fastapi
uvicorn
requests
langchain
langgraph
tiktoken
python-dotenv
langchain-openai
langchain-core

## 4. Start the MCP Server
Run the server in one terminal window:
```bash
uvicorn mcp_server:app --reload
```
Server runs at: http://localhost:8000

## 5. Start/Run the MCP Client
In a second terminal window, run the chat client:
```bash
python mcp_client.py
```

You can now chat with Adam interactively!

## Sample Interaction (5+ Turns)
```text
You: Hello Adam, who are you?
Adam: Greetings, traveler. I am Adam, a sage of the northern isles, here to share wisdom and stories with those who seek.

You: What are the different genres in gaming?
Adam: (fetches info from Wikipedia and responds)

You: Tell me a story from the ancient times.
Adam: Long ago, in lands beyond the known seas...

You: Who was the first king of the northern isles?
Adam: (fetches info if available, otherwise improvises)

You: Thank you, Adam.
Adam: May your journey be guided by the stars. Farewell for now.
```


### Features
- Custom Model Context Protocol (MCP)
  - Add and retrieve conversation history
  - Summarize old dialogues to manage token limits
  - Reset conversation memory
  - Perform factual lookups using Wikipedia API

- LangGraph Dialogue Flow
  - Input ➡️ Context Check ➡️ Tool Call (if needed) ➡️ Prompt Assembly ➡️ LLM Response ➡️ Output

- Token Management
  - Ensures total conversation fits within 4K token limits
  - Summarizes or prunes old dialogues intelligently

- Tool Use
  - If the player asks factual questions ("what is", "who is", etc.), Adam fetches real-world info from Wikipedia.

