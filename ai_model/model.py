from langchain_core.prompts import PromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate, \
    ChatPromptTemplate

from book.content import Content


class Model:
    """
    AI的模型对象的父类
    """

    def create_llm(self):
        print('初始化大语言模型的对象')

    def make_prompt(self):
        """
        创建提示词模板
        """
        system_template = """你是一个翻译专家，精通各种人类语言。
        输入的语种是：{source_language}，输出的语种是：{target_language}。
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
        human_message_prompt = HumanMessagePromptTemplate.from_template('{text}')

        prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

        return prompt

        # if content.content_type == ContentType.TEXT:
        #     return f'请翻译成{target_language}: {content.original}'
        # if content.content_type == ContentType.TABLE:
        #     return f'请翻译成{target_language}，每个元素之间用逗号隔开，以非MarkDown的表格形式返回：\n {content.get_original_to_string()}'
