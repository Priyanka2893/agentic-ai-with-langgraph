from langgraph.graph import StateGraph, START, END
from src.agenticchatbot.states.state import State
from src.agenticchatbot.nodes.basic_chatbot_node import BasicChatBotNode


class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Build a basic chatbot graph using langgraph
        This method initialises a chatbot node using the 'BasicChatBotNode' class
        and integrates it into graph. the chatbot node is 
        set as both the entry and exit point of graph
        """

        self.basic_chatbot_node=BasicChatBotNode(self.llm)
        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)