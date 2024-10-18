from typing import Annotated, Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from langchain_openai import ChatOpenAI

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    sender: str
    count: int

def reader_call(state:AgentState):
    name = "reader"
    reader_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a resume reading and preparing assistant. You will be given the contents of the resume that is parsed with a particular file reader.
         You are expected to prepare the resume data for processing further. The document should contain its originality and you should only beautify it.
         Also you are not expected to provide any headers like 'Here is the resume' or any footers like 'This resume format maintains the originality of the content'. Instead just provide only the content.
         Remember that you are a part of a team. So you are expected to present file contents properly without any changes that affects the context."""),
        ("human", "{input}")
    ])
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    reader_chain = reader_prompt | llm

    response = reader_chain.invoke({"input": state['messages']})
    return {
        "messages": [response.content],
        "sender": name,
        "count": state.get("count", 0)
    }
