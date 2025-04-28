# --- Imports ---
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langchain.prompts import PromptTemplate
import requests
from dotenv import load_dotenv
import tiktoken
from typing import TypedDict, Optional

# --- Load environment ---
load_dotenv()

# --- Define Adam's persona ---
persona = "Adam is a wise, centuries-old sage from the northern isles. He speaks with empathy and shares ancient lore."

# --- Initialize LLM ---
llm = ChatOpenAI(model="gpt-3.5-turbo")

# --- Tokenizer ---
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

def count_tokens(text: str) -> int:
    """Accurately count the number of tokens in a text."""
    return len(tokenizer.encode(text))

def summarize_history(history_text: str) -> str:
    """(Optional) Summarize long conversation history."""
    # Here, a real call to llm could happen.
    lines = history_text.split("\n")
    if len(lines) > 10:
        return "\n".join(lines[-10:])  # Keep last 10 lines
    return history_text

# --- Nodes ---

# 1. Context Fetch Node
def check_context_node(state):
    try:
        res = requests.get("http://localhost:8000/get_context")
        context = res.json().get("context", [])
    except Exception as e:
        print("[ERROR] Failed to get context:", e)
        context = []

    state["context"] = context
    return state

# 2. Tool Decision Node
def tool_decision_node(state):
    question = state["user_input"].lower()
    if any(kw in question for kw in ["what is", "who is", "types of", "genres", "explain"]):
        state["_next"] = "tool_call"
    else:
        state["_next"] = "assemble_prompt"
    return state

# 3. Tool Call Node
def tool_call_node(state):
    query = state["user_input"]
    try:
        res = requests.get(f"http://localhost:8000/tool_call", params={"query": query})
        state["tool_result"] = res.json().get("result", "")
    except Exception as e:
        print("[ERROR] Tool call failed:", e)
        state["tool_result"] = ""
    return state

# 4. Assemble Prompt Node
def assemble_prompt_node(state):
    template = PromptTemplate.from_template(
        "{persona}\n\nConversation so far:\n{history}\n\nPlayer: {user_input}\nAdam:"
    )
    history_messages = state.get("context", [])
    history_text = "\n".join([f'{m["role"]}: {m["content"]}' for m in history_messages])

    total_tokens = count_tokens(history_text)
    if total_tokens > 3500:
        print("[INFO] Summarizing history due to token limit...")
        history_text = summarize_history(history_text)

    if state.get("tool_result"):
        history_text += f"\nTool: {state['tool_result']}"

    prompt = template.format(
        persona=persona,
        history=history_text,
        user_input=state["user_input"]
    )

    state["final_prompt"] = prompt
    state["_next"] = "llm"
    return state

# 5. LLM Node: Generate Adam's reply
def llm_node(state):
    if not state.get("final_prompt"):
        raise ValueError("[ERROR] No final prompt available for LLM!")

    response = llm.invoke(state["final_prompt"])
    state["llm_output"] = response.content.strip()
    return state

# 6. Output Node: Print Adam's reply and save to memory
def output_node(state):
    print(f"Adam: {state['llm_output']}\n")

    # Update memory
    try:
        requests.post("http://localhost:8000/add_message", json={"role": "user", "content": state["user_input"]})
        requests.post("http://localhost:8000/add_message", json={"role": "assistant", "content": state["llm_output"]})
    except Exception as e:
        print("[ERROR] Failed to update memory:", e)

    return state

# --- State Definition ---

class ConversationState(TypedDict):
    user_input: Optional[str]
    context: Optional[list]
    tool_result: Optional[str]
    final_prompt: Optional[str]
    llm_output: Optional[str]
    _next: Optional[str]

# --- Build Workflow ---

workflow = StateGraph(ConversationState)

# --- Add nodes --- 
workflow.add_node("check_context", check_context_node)
workflow.add_node("tool_decision", tool_decision_node)
workflow.add_node("tool_call", tool_call_node)
workflow.add_node("assemble_prompt", assemble_prompt_node)
workflow.add_node("llm", llm_node)
workflow.add_node("output", output_node)

# --- Set entry point --- 

workflow.set_entry_point("check_context")

# --- Add edges --- 

workflow.add_edge("check_context", "tool_decision")
workflow.add_conditional_edges(
    "tool_decision",
    lambda state: state["_next"],
    {
        "tool_call": "tool_call",
        "assemble_prompt": "assemble_prompt",
    }
)
workflow.add_edge("tool_call", "assemble_prompt")
workflow.add_edge("assemble_prompt", "llm")
workflow.add_edge("llm", "output")

# --- Compile the graph --- 
app = workflow.compile()

# --- Conversation Loop ---

while True:
    user_input = input("Player: ")
    if user_input.lower() == "exit":
        print("Ending conversation.")
        break

    initial_state = {
        "user_input": user_input,
        "context": None,
        "tool_result": None,
        "final_prompt": None,
        "llm_output": None,
        "_next": None,
    }
    app.invoke(initial_state)
