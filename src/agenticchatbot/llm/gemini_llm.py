import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

class GeminiLLM:
    def __init__(self, user_control_input):
        self.user_control_input = user_control_input

    def get_llm_model(self):
        try:
            gemini_api_key = self.user_control_input["GEMINI_API_KEY"]
            selected_gemini_model = self.user_control_input["selected_gemini_model"]
            if gemini_api_key == '' and os.environ.get("GEMINI_API_KEY", '') == '':
                st.error("Please enter the Gemini API key")

            llm = ChatGoogleGenerativeAI(google_api_key=gemini_api_key, model=selected_gemini_model)
        except Exception as e:
            raise ValueError(f"Error occurred with exception: {e}")

        return llm
