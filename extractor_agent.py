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

def extractor_call(state:AgentState):
    name = "extractor"
    extractor_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a resume parsing assistant. You will be given contents of the resume. You are expected to extract various information such as:
        1. Personal Information
        2. Education
        3. Work Experience
        4. Skills
        Compile the validated entities into a predefined JSON format for downstream use.
        Remember that you are a part of a team. So you are expected to read the file contents properly and you are expected to give the data properly.
        If the extraction is not up to the mark, you will be reprompted to extract that particular values again."""),
        ("human", "{input}")
    ])
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    extractor_chain = extractor_prompt | llm

    response = extractor_chain.invoke({"input": state['messages']})
    
    new_count = state.get("count", 0) + 1
    
    return {
        "messages": [response.content],
        "sender": name,
        "count": new_count
    }
