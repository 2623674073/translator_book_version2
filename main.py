from translator.book_translator import PDFTranslator
from ai_model.openai_model import OpenAIModel
from ai_model.glm_model import ChatGLMModel
from utils.project_config import ProjectConfig
import gradio as gr

if __name__ == '__main__':
    # # 1. 无页面版本
    # print('项目启动！！！')
    #
    # # 项目整体配置参数
    # config = ProjectConfig()
    # config.initialize()
    #
    # # 初始化大语言模型
    # if config.model_type == 'OpenAIModel':
    #     model = OpenAIModel(config.model_name, config.api_key, config.base_url)
    # else:
    #     model = ChatGLMModel(config.model_name, config.api_key, config.base_url)
    #     pass
    #
    # # 初始化一个翻译器
    # translator = PDFTranslator(model)
    # translator.book_tranlattion(file_path=config.input_file, out_file_format=config.file_format,
    #                             source_language=config.source_language, target_language=config.target_language)

    # 2. gradio可视化页面版本
    def translate_pdf(file, model_type, source_language, target_language, file_format):
        print('项目启动！！！')

        # 项目整体配置参数
        config = ProjectConfig()
        config.initialize()

        # 根据可视化页面动态覆盖配置参数
        config.input_file = file.name
        config.model_type = model_type
        config.source_language = source_language
        config.target_language = target_language
        config.file_format = file_format

        # 初始化大语言模型
        if config.model_type == 'OpenAIModel':
            model = OpenAIModel(config.model_name, config.api_key, config.base_url)
        else:
            model = ChatGLMModel(config.model_name, config.api_key, config.base_url)
            pass

        # 初始化一个翻译器
        translator = PDFTranslator(model)
        out_filepath = translator.book_tranlattion(file_path=config.input_file,
                                                   out_file_format=config.file_format,
                                                   source_language=config.source_language,
                                                   target_language=config.target_language)
        # print(f"翻译完成，输出路径: {out_filepath}")
        return out_filepath


    # 定义 Gradio 界面
    interface = gr.Interface(
        fn=translate_pdf,  # 我们刚刚定义的翻译函数
        inputs=[
            gr.File(label="上传 PDF 文件", type="filepath"),  # 上传文件
            gr.Radio(choices=["OpenAIModel", "ChatGLMModel"], label="选择模型类型"),
            gr.Dropdown(choices=["Chinese", "English", "Japanese", "Korean"], label="源语言"),
            gr.Dropdown(choices=["Chinese", "English", "Japanese", "Korean"], label="目标语言"),
            gr.Radio(choices=["md", "pdf", "其他待开发"], label="输出格式"),
        ],
        outputs=gr.File(label="下载翻译后的文件"),
        title="📚 PDF 文档翻译器",
        description="上传 PDF 文件，选择语言和模型，一键翻译。",
        allow_flagging="never"
    )

    # 启动服务
    interface.launch(share=True)  # share=True 自动生成公网访问链接
