import gradio as gr

from ai_model.glm_model import ChatGLMModel
from ai_model.openai_model import OpenAIModel
from translator.book_translator import PDFTranslator
from utils.project_config import ProjectConfig


def translate_pdf(file, model_type, source_lang, target_lang, out_format):
    print("开始翻译...")

    # 初始化配置
    config = ProjectConfig()
    config.initialize()

    # 动态覆盖配置参数
    config.input_file = file.name
    config.model_type = model_type
    config.source_language = source_lang
    config.target_language = target_lang
    config.file_format = out_format

    # 初始化模型
    if config.model_type == 'OpenAIModel':
        model = OpenAIModel(config.model_name, config.api_key, config.base_url)
    else:
        model = ChatGLMModel(config.model_name, config.api_key, config.base_url)

    # 初始化翻译器并执行翻译
    translator = PDFTranslator(model)
    output_path = translator.book_tranlattion(
        file_path=config.input_file,
        out_file_format=config.file_format,
        source_language=config.source_language,
        target_language=config.target_language
    )

    return output_path


# 定义 Gradio 界面
interface = gr.Interface(
    fn=translate_pdf,  # 我们刚刚定义的翻译函数
    inputs=[
        gr.File(label="上传 PDF 文件", type="filepath"),  # 上传文件
        gr.Radio(choices=["OpenAIModel", "ChatGLMModel"], label="选择模型类型"),
        gr.Dropdown(choices=["Chinese", "English", "Japanese", "Korean"], label="源语言"),
        gr.Dropdown(choices=["Chinese", "English", "Japanese", "Korean"], label="目标语言"),
        gr.Radio(choices=["md", "pdf","其他待开发"], label="输出格式"),
    ],
    outputs=gr.File(label="下载翻译后的文件"),
    title="📚 PDF 文档翻译器",
    description="上传 PDF 文件，选择语言和模型，一键翻译。",
    allow_flagging="never"
)

# 启动服务
if __name__ == "__main__":
    interface.launch(share=True)  # share=True 自动生成公网访问链接