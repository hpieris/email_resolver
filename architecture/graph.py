# architecture.py

from langgraph.graph import StateGraph, END
from typing import TypedDict

# Define shared state
class AgentState(TypedDict):
    email_text: str
    classification: str
    draft: str
    approved_response: str
    sent: bool

# Dummy agents for simulation
def email_classifier(state: AgentState) -> AgentState:
    print("📥 email_classifier running...")
    return {**state, "classification": "Complaint - Urgent"}

def response_drafter(state: AgentState) -> AgentState:
    print("📝 response_drafter running...")
    return {**state, "draft": "We're sorry for the inconvenience. We are working on it."}

def approver(state: AgentState) -> AgentState:
    print("✅ approver running...")
    return {**state, "approved_response": f"Approved: {state['draft']}"}

def emailer(state: AgentState) -> AgentState:
    print("📤 emailer running...")
    return {**state, "sent": True}

# Define the LangGraph
def get_graph():
    graph = StateGraph(AgentState)

    graph.add_node("email_classifier", email_classifier)
    graph.add_node("response_drafter", response_drafter)
    graph.add_node("approver", approver)
    graph.add_node("emailer", emailer)

    graph.set_entry_point("email_classifier")
    graph.add_edge("email_classifier", "response_drafter")
    graph.add_edge("response_drafter", "approver")
    graph.add_edge("approver", "emailer")
    graph.add_edge("emailer", END)

    return graph.compile()

# Optional test run
if __name__ == "__main__":
    app = get_graph()
    final = app.invoke({"email_text": "I am very unhappy with the product I received."})
    print("\n✅ Final state:\n", final)
