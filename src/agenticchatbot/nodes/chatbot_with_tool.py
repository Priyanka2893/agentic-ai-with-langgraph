from agenticchatbot.states.state import State

class ChatBotWithTool:
    def __init__(self,model):
        self.llm=model

    def process(self,state:State):
        """
        Processes the input state and generates a response with tool integration
        """

        user_input = state['messages'][-1] if state['messages'] else ""
        llm_response = self.llm.invke([{'role':'user',"content":user_input}])

        tools_response = f"Tool integration for {user_input}"

        return {'messages':[llm_response,tools_response]}
    
    def create_chatbot(self,tools):
        """
        return chatbot node function
        """

        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state:State):
            return {'messages':[llm_with_tools.invoke(state['messages'])]}
        
        return chatbot_node