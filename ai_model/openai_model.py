import time

from langchain_openai import ChatOpenAI
from ai_model.model import Model


class OpenAIModel(Model):

    def __init__(self, model_name: str, api_key: str, base_url: str):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url

    def create_llm(self):

        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=self.api_key,
            base_url=self.base_url,
            # organization="...",
            # other params...
        )

        return llm

