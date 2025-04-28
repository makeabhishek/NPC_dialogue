# NPC Dialogue System Using Model Context Protocol (MCP)

## Adam the Sage — NPC Dialogue System

#### Overview
This project develops a context-aware dialogue engine for a Role-Playing Game (RPG) NPC (Non-Player Character) named **Adam**, using a custom **Model Context Protocol (MCP)**, LangGraph for dialogue routing, and GPT-based conversations. It integrates three core components:

- __Model Context Protocol (MCP):__
A custom server that manages conversation memory, handles summarization, and provides context-aware responses within token limits.

- __LangGraph Orchestration:__
A state-based workflow that routes dialogue steps, including context retrieval, tool usage, prompt assembly, and LLM invocation.

- __GPT-3.5-Turbo:__
Powers Adam's conversational abilities, generating responses based on player input, context history, and factual lookups.

Adam serves as an NPC player who interacts intelligently with players, remembers previous conversations, and it can leverages external tools (like Wikipedia search) when necessary.

__Dialogue Example:__ Adam is a centuries-old, wise sage from the northern isles who speaks with empathy and shares ancient lore.

---

## Project Structure
/NPC_dialogue_project/ \
├── mcp_server.py     # MCP Server - handles context, memory, and tool use \
├── mcp_client.py     # MCP Client - chat interface with LangGraph workflow  \
├── .env              # Secret API keys  \
├── requirements.txt  # Required Python libraries \
├── README.md         # Setup instructions and description 

---

## Setup Instructions
To Set This Up Locally

### 1. Clone / Download Project
Clone this repo or download the files into a folder.

### 2. Create `.env` File for API KEYS
Create a `.env` file in your project folder with this content:

```env
OPENAI_API_KEY="your-openai-api-key-here"
```

- Replace `your-openai-api-key-here` with your actual OpenAI key.

## 3. Install Dependencies
### Virtual environemnt 
Create virtual environemnt (-y for default packages installation)
```python
conda create -p venv python==3.10 -y
conda activate venv
```

### Requirements file
`requirements.txt`. Install all required Python libraries using:
```bash
pip install -r requirements.txt
```

## 4. Start the MCP Server
Run the server in one terminal window:
```bash
uvicorn mcp_server:app --reload --port 8000
```
Server runs at: http://localhost:8000

## 5. Start/Run the MCP Client
In a second terminal window, run the chat client:
```bash
python mcp_client.py
```

To manage tokens, run
```bash
python mcp_client_tokenMgmt.py
```
Section "Tokenizer" is the modification to manage the tokens and than in the Assemble Prompt Node.

You can now chat with **Adam** interactively!

## Sample Interaction (5+ Turns)
`NPCdialogueResponse.txt`contains sample interations
```text

Player: hello Adam
Adam: Greetings, young one. How may I be of service to you today?

Player: Tell me about the northern isles.
Adam: Ah, the northern isles are a place of immense beauty and mystery. The ancient lore of the land is rich with wisdom passed down through generations. The people of the northern isles are strong and resilient, shaped by the harsh yet captivating landscape that surrounds them. From the rugged cliffs overlooking the icy seas to the lush green valleys dotted with ancient ruins, the northern isles hold a certain mystique that has captivated the hearts of many throughout history. It is a land of contrasts, where the elements themselves seem to come alive in a dance of power and grace. It is a place where the veil between the mundane world and the realm of magic is thin, and those who journey there often find themselves forever changed.

Player: What are the different genres in gaming?
Adam: Ah, the world of gaming is vast and diverse, young one. There are many different genres that cater to a wide range of tastes and preferences. Some popular genres include action, adventure, role-playing, strategy, simulation, and more. Each genre offers unique gameplay experiences and challenges for players to enjoy. It is truly a realm where one can explore new worlds, face towering foes, and embark on epic quests unlike any other. Tell me, which gaming genre interests you the most?

Player:  I feel lost.
Adam: It is not uncommon to feel lost at times, my dear friend. Life can be overwhelming and confusing, but remember that you are never truly alone. Take a deep breath and center yourself in this moment. Reflect on what truly matters to you and what brings you joy and fulfillment. Sometimes, simply taking a step back and gaining a new perspective can help you find your way. Trust in yourself and your inner wisdom, for you have the strength and resilience to navigate through any challenges that come your way. And remember, even in the darkest of times, there is always a glimmer of hope and light waiting to guide you on your path.

Player: Thank you, Adam.
Adam: You are most welcome, my friend. Remember, I am always here to offer guidance and support whenever you need it. May you find peace and clarity on your journey ahead.
```

#### Sample Interaction after tokenization (5+ Turns)
```text

(C:\Users\makea\OneDrive\Python\NPC_dialogue\venv) C:\Users\makea\OneDrive\Python\NPC_dialogue>python mcp_client_tokenMgmt.py

Player: hi adam
Adam: Greetings, traveler. How may I assist you today?

Player: Tell me about the northern isles.
Adam: The northern isles are a land of mystery and beauty, filled with rugged mountains, deep forests, and cold seas. The people who live there are hardy and resourceful, and they have a deep connection to the land and the spirits that dwell within it. The ancient lore of the northern isles tells of great heroes and epic battles, of magic and wonder. It is a place where the past is always present, and where the spirits of the land still walk among us.

Player: What are the different genres in gaming?
Adam: Ah, gaming is a vast and diverse world, filled with many genres to suit every taste and preference. Some common genres include action, adventure, role-playing, strategy, puzzle, and simulation. Each genre offers a unique gameplay experience and challenges players in different ways. Whether you prefer to immerse yourself in fantastical worlds, test your reflexes in fast-paced action games, or exercise your strategic thinking in complex simulations, there is a genre of gaming that is sure to captivate you. The choice is yours, adventurer.

Player: I feel lost.
Adam: It's not uncommon to feel lost at times, my friend. Life is a journey full of twists and turns, and it's natural to feel unsure of where you're headed. Remember, it's okay to ask for help and seek guidance from those around you. Take a moment to pause, reflect, and connect with your inner wisdom. Trust that you have the strength and resilience to navigate through any challenges that come your way. You are not alone on this journey, and there are always allies and support waiting to guide you. Trust in yourself and the path will become clearer.

Player: Thank you, Adam.
Adam: You're welcome, my friend. Remember, even in the darkest of times, there is always a light to guide you. Trust in your inner wisdom and keep moving forward with courage and determination. May your journey be filled with wisdom and blessings. Safe travels, adventurer.

Player:

```
### Features
- Custom Model Context Protocol (MCP)
  - Add and retrieve conversation history
  - Summarize old dialogues to manage token limits
  - Reset conversation memory
  - Perform factual lookups using Wikipedia API

- LangGraph Dialogue Flow
  - Input $\rightarrow$ Context Check $\rightarrow$ Tool Call (if needed) $\rightarrow$ Prompt Assembly $\rightarrow$ LLM Response $\rightarrow$ Output

- Token Management
  - Ensures total conversation fits within 4K token limits
  - Summarizes or prunes old dialogues intelligently

- Tool Use
  - If the player asks factual questions ("what is", "who is", etc.), Adam fetches real-world info from Wikipedia.

