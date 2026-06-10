from langchain_core.messages import HumanMessage, AIMessage

from agenticchatbot.llm.openai_llm import OpenAILLM
from agenticchatbot.llm.gemini_llm import GeminiLLM
from agenticchatbot.llm.groq_llm import GroqLLM
from agenticchatbot.graph.graph_builder import GraphBuilder

# Maps UI provider name → LLM class + input dict keys
_PROVIDER_MAP = {
    "OpenAI": {
        "class": OpenAILLM,
        "api_key_field": "OPENAI_API_KEY",
        "model_field": "selected_openai_model",
    },
    "Google Gemini": {
        "class": GeminiLLM,
        "api_key_field": "GEMINI_API_KEY",
        "model_field": "selected_gemini_model",
    },
    "Groq": {
        "class": GroqLLM,
        "api_key_field": "GROQ_API_KEY",
        "model_field": "selected_groq_model",
    },
}


class AgenticChatbot:
    def __init__(self, provider: str, model: str, api_key: str, usecase: str):
        config = _PROVIDER_MAP[provider]
        user_control_input = {
            config["api_key_field"]: api_key,
            config["model_field"]: model,
        }
        llm = config["class"](user_control_input).get_llm_model()
        self.graph = GraphBuilder(llm).setup_graph(usecase)

    def chat(self, history: list[dict]) -> str:
        """
        history: list of {"role": "user"|"assistant", "content": "..."}
        Returns the latest assistant response as a string.
        """
        lc_messages = []
        for msg in history:
            if msg["role"] == "user":
                lc_messages.append(HumanMessage(content=msg["content"]))
            else:
                lc_messages.append(AIMessage(content=msg["content"]))

        result = self.graph.invoke({"messages": lc_messages})
        return result["messages"][-1].content
