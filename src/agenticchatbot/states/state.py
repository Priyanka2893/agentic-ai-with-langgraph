from typing_extentions import TypedDict
from langgraph.graph.message import add_messages
from typing import Annotated

class Satte(TypedDict):
    """
    Represent the structure of the state used in graph
    """
    message: Annotated[list, add_messages]

    