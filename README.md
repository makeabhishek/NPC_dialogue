
#-------------------------------------------#
# Adam Non-Player Character (NPC) Dialogue Engine
NPC Dialogue System Using Model Context Protocol (MCP)

## Overview
A context-aware RPG NPC named Adam using a custom MCP server, LangGraph orchestration, and GPT-3.5-turbo.

## Setup
1. Install dependencies:
pip install fastapi uvicorn langchain-openai langgraph requests tiktoken

2. Start MCP Server:

`uvicorn mcp_server:app --reload`
3. Run Client:

`python mcp_client.py`
## Persona
Adam is a wise, centuries-old sage from the northern isles. He speaks with empathy and shares ancient lore.

## Features
- Summarizes conversation history when nearing token limit.
- Uses Wikipedia for factual lookups.
- Maintains memory of player-NPC interactions.

## Example Dialogue

**Player:** Hello Adam.  
**Adam:** Greetings, traveler. The winds spoke of your arrival.

**Player:** Tell me about the northern isles.  
**Adam:** Ah, the northern isles, misty lands where ancient stones hum with forgotten magic.

**Player:** What are the different genres in gaming?  
**Adam:** (fetched via Wikipedia) There are many genres: action, adventure, RPG, simulation, and strategy.

**Player:** I feel lost.  
**Adam:** Even the mightiest trees sway in the storm. You'll find your footing.

**Player:** Thank you, Adam.  
**Adam:** May the stars watch over you, always.

4. requirements.txt
fastapi
uvicorn
requests
langchain-openai
langgraph
tiktoken

langchain
ipykernel
python-dotenv
langchain_community
pypdf
bs4 # beautiful soup
arxiv 


# To Set This Up Locally
1. Clone repo

2. Create virtual environemnt (-y for default packages installation)
`conda create -p venv python==3.10 -y`
`conda activate venv`

# Create .env file, whcih consist of 
OPENAI_API_KEY=" "
LANGCHAIN_API_KEY=" "
LANGCHAIN_PROJECT="GenAIAPP" 

3. Install dependencies:
`pip install -r requirements.txt`

4. Start MCP Server:
`uvicorn mcp_server:app --reload`

4. Run Client:
`python mcp_client.py`
