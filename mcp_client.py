# Import necessary libraries
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langchain.prompts import PromptTemplate
import requests
from dotenv import load_dotenv
load_dotenv()

# Define Adam's persona
persona = "Adam is a wise, centuries-old sage from the northern isles. He speaks with empathy and shares ancient lore."

# Initialize the LLM (GPT-3.5-Turbo)
llm = ChatOpenAI(model="gpt-3.5-turbo")

# 1. Context Fetch Node: Fetch conversation memory
def check_context_node(state):
    res = requests.get("http://localhost:8000/get_context")
    state["context"] = res.json()["context"]
    return state    #

# 2. Tool Decision Node: Should we call Wikipedia?
def tool_decision_node(state):
    question = state["user_input"].lower()
    if any(kw in question for kw in ["what is", "who is", "types of", "genres", "explain"]):
        state["_next"] = "tool_call"     # store next node inside state
    else:
        state["_next"] = "assemble_prompt"    #
    return state    #

# 3. Tool Call Node: Call Wikipedia if needed
def tool_call_node(state):
    query = state["user_input"]
    res = requests.get(f"http://localhost:8000/tool_call", params={"query": query})
    state["tool_result"] = res.json()["result"]
    return state    #

# 4. Assemble Prompt Node: Build final prompt
def assemble_prompt_node(state):
    template = PromptTemplate.from_template(
        "{persona}\n\nConversation so far:\n{history}\n\nPlayer: {user_input}\nAdam:"
    )
    history = "\n".join([f'{m["role"]}: {m["content"]}' for m in state["context"]])

    if state.get("tool_result"):
        history += f"\nTool: {state['tool_result']}"

    prompt = template.format(persona=persona, history=history, user_input=state["user_input"])
    state["final_prompt"] = prompt
    return state    # 

# 5. LLM Node: Generate Adam's reply
def llm_node(state):
    response = llm.invoke(state["final_prompt"])
    state["llm_output"] = response.content
    return state    # 

# 6. Output Node: Print Adam's reply and save to memory
def output_node(state):
    print(f"Adam: {state['llm_output']}")

    requests.post("http://localhost:8000/add_message", json={"role": "user", "content": state["user_input"]})
    requests.post("http://localhost:8000/add_message", json={"role": "assistant", "content": state["llm_output"]})
    
    return state    #

# Define the State
from typing import TypedDict, Optional

class ConversationState(TypedDict):
    user_input: Optional[str]
    context: Optional[list]
    tool_result: Optional[str]
    final_prompt: Optional[str]
    llm_output: Optional[str]
    _next: Optional[str]   # needed to support branching!

# Build the workflow
workflow = StateGraph(ConversationState)

# Add nodes
workflow.add_node("check_context", check_context_node)
workflow.add_node("tool_decision", tool_decision_node)
workflow.add_node("tool_call", tool_call_node)
workflow.add_node("assemble_prompt", assemble_prompt_node)
workflow.add_node("llm", llm_node)
workflow.add_node("output", output_node)

# Set entry point
workflow.set_entry_point("check_context")

# Add edges
workflow.add_edge("check_context", "tool_decision")
workflow.add_conditional_edges(
    "tool_decision",
    lambda state: state["_next"],    # use the _next value to choose branch
    {
        "tool_call": "tool_call",
        "assemble_prompt": "assemble_prompt",
    },
)
workflow.add_edge("tool_call", "assemble_prompt")
workflow.add_edge("assemble_prompt", "llm")
workflow.add_edge("llm", "output")

# Compile the graph
app = workflow.compile()

# Conversation loop
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
        "_next": None,   # initialize _next
    }
    app.invoke(initial_state)
