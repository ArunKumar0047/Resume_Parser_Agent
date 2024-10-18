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

def validator_call(state:AgentState):
    name = "validator"
    validator_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a parsed resume validation assistant. You will be given the extracted entities from the resume.
                 Perform quality checks and ensure that the fields match with the actual content.
                 So provide corrections that the other agent will then look at and then extract them correctly.
         If there are quality errors, then provide them as a set of bullet points.
                Remember that you are a part of a team. So you are expected to present the corrections properly without any unwanted changes.
                 If you don't notice any changes or mistakes then just return 'Yes'. Also you should not provide any headers or additional information like 'There is no mistake', 'The extraction is correct', etc. Just provide the final 'Yes'."""),
        ("human", "{input}"),
    ])
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    validator_chain = validator_prompt | llm

    response = validator_chain.invoke({"input": state['messages']})
    
    return {
        "messages": [response.content],
        "sender": name,
        "count": state.get("count", 0)
    }
