import os

import yaml

from utils.argument_utils import ArgumentUtils


class ProjectConfig:
    """
    统一处理整个项目的配置,  整个项目的配置对象设置为单例
    """

    _instance = None  # 是一个类级别的变量（也叫静态变量），用于保存 ProjectConfig 类的唯一实例

    def __init__(self):
        self._config = None
        self._args = None

    def __new__(cls, *args, **kwargs):
        """
        实现了单例模式，确保 ProjectConfig 类在整个程序运行期间只存在一个实例。
        具体实现方式是通过重写类的 new 方法
        cls: 表示当前类本身

        如果为 None，说明这是第一次创建对象，需要生成一个新的实例；
        否则，直接返回已有的实例。
        """
        if cls._instance is None:
            cls._instance = super(ProjectConfig, cls).__new__(cls)

        return cls._instance

    def initialize(self):
        """
        初始化所有的项目配置
        :return:
        """

        # 环境变量配置的初始化
        os.environ['http_proxy'] = '127.0.0.1:7890'
        os.environ['https_proxy'] = '127.0.0.1:7890'

        # 命令行参数 配置的初始化
        if self._args is None:
            args_utils = ArgumentUtils()
            self._args = args_utils.parser_arg()

        # YAML文件 配置的初始化： 如果YAML中的配置和命令行参数冲突，以命令参数为准
        if self._config is None:
            with open(self._args.config, 'r') as f:
                config = yaml.safe_load(f)

            overridden_config = {  # 所有冲突的配置 字典
                key: value for key, value in vars(self._args).items() if key in config and value is not None
            }

            config.update(overridden_config)       # 把命令的参数覆盖 config文件里面的
            self._config = config

    def __getattr__(self, item):
        # 当访问当前对象实例的属性时 自动调用  self.model_name
        if self._config and item in self._config:
            return  self._config[item]
        raise AttributeError(f'项目配置中没有一个属性：{item}')