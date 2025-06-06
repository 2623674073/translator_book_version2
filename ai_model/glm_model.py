from openai import OpenAI

from ai_model.model import Model


class ChatGLMModel(Model):

    def __init__(self, model_name: str, api_key: str, base_url: str):
        self.model_name = model_name
        self.api_key = api_key
        self.base_url = base_url

    def create_llm(self):
        # llm = ChatOpenAI(     # 换一下模型接口即可
        #     model="gpt-4o",
        #     temperature=0,
        #     max_tokens=None,
        #     timeout=None,
        #     max_retries=2,
        #     api_key=self.api_key,
        #     base_url=self.base_url,
        #     # organization="...",
        #     # other params...
        # )
        #
        # return llm

        pass

    