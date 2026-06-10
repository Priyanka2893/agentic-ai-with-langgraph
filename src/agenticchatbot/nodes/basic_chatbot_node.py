from src.agenticchatbot.states.state import State

class BasicChatBotNode:
    """
    Basic Chatbot login implementation
    """

    def __init__(self,model):
        self.llm=model
    
    def process(self, state:State) -> dict:
        """
        Processes the input and generates the output
        """

        return {"messages" :self.llm.invoke(state['messages'])}
    
    
