from ai_model.model import Model
from book.content import Content, ContentType
from utils.log_utils import log


class TranslatorChain:
    """
    负责调用langchain来完成文本的翻译， chain对象，要不要是单例的？   要，因为每次调用时再重新初始化回很浪费资源
    """
    _instance = None

    def __init__(self, model: Model):

        self.langchain = model.make_prompt() | model.create_llm()

    def __new__(cls, *args, **kwargs):
        """
        实现了单例模式，确保 TranslatorChain 类在整个程序运行期间只存在一个实例。
        具体实现方式是通过重写类的 new 方法
        cls: 表示当前类本身

        如果为 None，说明这是第一次创建对象，需要生成一个新的实例；
        否则，直接返回已有的实例。
        """
        if cls._instance is None:
            cls._instance = super(TranslatorChain, cls).__new__(cls)

        return cls._instance

    def run(self, content: Content, source_language: str, target_language: str):
        """
        翻译具体的文本，返回翻译之后的文本内容和翻译成功的状态
        :param content:
        :param source_language:
        :param target_language:
        :return: translation_text, status
        """

        text = " "
        result = " "

        try:
            # 提示模板中的三个变量
            if content.content_type == ContentType.TEXT:
                text = f"请按照要求翻译以下的内容: {content.original}"
            elif content.content_type == ContentType.TABLE:
                log.info("+++++++++++++")
                text = f'请按照要求翻译以下的内容，每个元素之间用逗号隔开，以非MarkDown的表格形式返回：\n {content.get_original_to_string()}'

            result = self.langchain.invoke({
                'source_language':source_language,
                'target_language':target_language,
                'text':text
            })
            log.info(result.content)
        except Exception as e:
            log.exception(e)
            return result, False  # 报错的返回
        return result.content, True


