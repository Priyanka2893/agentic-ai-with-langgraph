from langgraph.graph import StateGraph, START, END
from agenticchatbot.states.state import State
from agenticchatbot.nodes.basic_chatbot_node import BasicChatBotNode
from agenticchatbot.tools.search_tool import get_tools,create_tool_node
from langgraph.prebuilt import tools_condition
from agenticchatbot.nodes.chatbot_with_tool import ChatBotWithTool 
from agenticchatbot.nodes.ai_news_node import AINode

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

    def setup_graph(self, chatbot_type: str = "Basic Chatbot"):
        """
        Builds and compiles the graph for the given chatbot type.
        Returns the compiled graph ready for invocation.
        """
        if chatbot_type == "Chatbot with Tools":
            self.chatbot_with_tools_build_graph()
        elif chatbot_type == "AI News":
            self.ai_news_builder_graph()
        else:
            self.basic_chatbot_build_graph()
        return self.graph_builder.compile()

    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot with tool integration.
        Flow: chatbot → (conditional) → tools → chatbot → END
        """
        tools = get_tools()
        tool_node = create_tool_node(tools)
        obj_chatbot = ChatBotWithTool(self.llm)
        chatbot = obj_chatbot.create_chatbot(tools)

        self.graph_builder.add_node("chatbot", chatbot)
        self.graph_builder.add_node("tools", tool_node)

        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")

    def ai_news_builder_graph(self):
        ai_node = AINode(self.llm)
        # nodes
        
        self.graph_builder.add_node("fetch_news",ai_node.fecth_news)
        self.graph_builder.add_node("summarize_news",ai_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_node.save_result)

        # edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)


