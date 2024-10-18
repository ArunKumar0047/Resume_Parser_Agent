from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

from agents.reader_agent import reader_call
from agents.extractor_agent import extractor_call
from agents.validator_agent import validator_call

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    sender: str
    count: int

def router(state: AgentState):
    if state.get("count", 0) >= 3 or state["messages"][-1].content == 'Yes':
        return END
    elif state["sender"] == "reader":
        return "extractor"
    elif state["sender"] == "extractor":
        return "validator"
    elif state["sender"] == "validator":
        return "extractor"
    else:
        return "reader"

def create_workflow():
    workflow = StateGraph(AgentState)

    workflow.add_node("reader", reader_call)
    workflow.add_node("extractor", extractor_call)
    workflow.add_node("validator", validator_call)

    workflow.add_edge(START, "reader")

    workflow.add_conditional_edges(
        "reader",
        router,
        {
            "extractor": "extractor",
            END: END
        }
    )

    workflow.add_conditional_edges(
        "extractor",
        router,
        {
            "validator": "validator",
            END: END
        }
    )

    workflow.add_conditional_edges(
        "validator",
        router,
        {
            "extractor": "extractor",
            END: END
        }
    )


    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)

    return app
