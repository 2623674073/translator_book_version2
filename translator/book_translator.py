from ai_model.model import Model
from typing import Optional

from book.content import ContentType
from translator.file_writer import FileWriter
from translator.pdf_parser import parse_pdf
from translator.translator_chain import TranslatorChain

from utils.log_utils import log


class PDFTranslator:
    """
    翻译pdf文件的书籍
    """

    def __init__(self, model: Model):

        self.book = None
        self.writer = FileWriter(self.book)
        self.chain = TranslatorChain(model)

    def book_tranlattion(self, file_path: str, out_file_format: str, source_language: str, target_language: str,
                         out_file_path: str = None, pages: Optional[int] = None):
        """
        翻译一本书
        :param file_path:
        :param out_file_format:
        :param source_language:
        :param target_language:
        :param out_file_path:
        :param pages:   要翻译的页数
        :return:
        """

        self.book = parse_pdf(pdf_filf_path=file_path, pages=pages)
        self.writer.book = self.book

        for page_index, page in enumerate(self.book.pages):
            for content_index, content in enumerate(page.contents):
                # 只对 TEXT 和 TABLE 类型的内容执行翻译
                if content.content_type in (ContentType.TEXT, ContentType.TABLE):
                    # 开始翻译每一页的每一个内容
                    translation_text, status = self.chain.run(content, source_language=source_language,
                                                              target_language=target_language)

                    log.debug(f'翻译之后的内容是: \n {translation_text}')
                    # 把翻译之后的文本和状态设置到content对象中 （保存）
                    self.book.pages[page_index].contents[content_index].set_translation(translation_text, status)

                elif content.content_type == ContentType.IMAGE:
                    # 图像内容不翻译，直接跳过
                    content.set_status(True)  # ← 关键操作
                    log.debug("检测到图像内容，跳过翻译")
                    continue

        print(f"out_file_path {out_file_path} out_file_format{out_file_format}")
        # out_file_path = file_path[:file_path.rfind('.')] + '_translated'+'.'+out_file_format.lower()
        # 把翻译之后的所以数据写入文件
        out_file_path = self.writer.save_book(out_file_path, out_file_format)

        # 返回生成文件的路径，供 Gradio 显示下载
        return out_file_path


