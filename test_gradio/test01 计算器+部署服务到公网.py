import os
from pyngrok import ngrok, conf
import gradio as gr

# 在代码中直接设置 ngrok 的认证 Token
os.environ["NGROK_AUTHTOKEN"] = "2y7xMYi0k9SbDUucpXFRHkHTazL_6K3GRCTCjJB8giApj32ch"
def calculator(num1, operation, num2):
    if operation == '加':
        return num1 + num2
    elif operation == '减':
        return num1 - num2
    elif operation == '乘':
        return num1 * num2
    elif operation == '除':
        if num2 == 0:
            raise gr.Error('0不能作为除数！')
        return num1 / num2


instance = gr.Interface(  # 构建一个UI界面
    fn=calculator,
    inputs=[
        'number',
        gr.Radio(choices=['加', '减', '乘', '除'], label='计算法则'),
        'number'
    ],
    outputs='number'
)


### 可以通过ngrok将服务部署到公网，需要关防火墙
# # 启动 ngrok 隧道
# public_url = ngrok.connect(addr="7860")  # Gradio 默认端口是 7860
# print(f"🌐 公网访问地址: {public_url}")
"""
🌐 公网访问地址: NgrokTunnel: "https://d164-175-172-153-85.ngrok-free.app" -> "http://localhost:7860"
* Running on local URL:  http://0.0.0.0:7860
* To create a public link, set `share=True` in `launch()`.
"""

# 启动服务
instance.launch(server_name='0.0.0.0', server_port=7860, auth=('admin', '123123'))


