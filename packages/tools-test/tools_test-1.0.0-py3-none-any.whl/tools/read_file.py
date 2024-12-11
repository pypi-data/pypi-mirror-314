import yaml
from tools import extractor


class ReadFile:
    """
    文件操作
    """
    config_dict = None

    @classmethod
    def get_config_dict(cls, config_path='config/config.yaml') -> dict:
        """
        读取配置文件，并且转换成字典,缓存至config_dict
        :param config_path: yaml文件地址， 默认使用当前项目目录下的config/config.yaml
        return cls.config_dict
        """
        if cls.config_dict is None:
            # 指定编码格式解决，win下跑代码抛出错误
            with open(config_path, 'r', encoding='utf-8') as file:
                cls.config_dict = yaml.load(
                    file.read(), Loader=yaml.FullLoader)
        return cls.config_dict

    @classmethod
    def read_config(cls, expr: str = '.'):
        """
        默认读取config目录下的config.yaml配置文件，根据传递的expr jsonpath表达式可任意返回任何配置项
        :param expr: 提取表达式, 使用jsonpath语法,默认值提取整个读取的对象
        return 根据表达式返回的值
        """
        return extractor(cls.get_config_dict(), expr)

    @classmethod
    def read_yaml(cls, path):
        """
        读取yaml文件
        :param path: 文件路径
        :return: 返回读取的文件数据，dict类型
        """

        # 指定编码格式解决，win下跑代码抛出错误
        with open(path, 'r', encoding='utf-8') as file:
            data = yaml.load(file.read(), Loader=yaml.FullLoader)

        return data
