"""
通用工具
"""
import shortuuid
import os
import yaml
import sys


def short_uuid():
    """
    生成短UUID
    :return:
    """
    return shortuuid.uuid()

def load_config(config_file = ''):
    """
    加载服务配置信息
    :return:
    """
    if config_file == '':
        project_root = sys.path[0]
        config_file = os.path.abspath(os.path.join(project_root, '.config.yml'))

    if not os.path.exists(config_file):
        raise FileNotFoundError('未找到本地配置文件 .config.yml，请创建该配置文件后再次尝试')
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

def config_value(config, key_path, default_value = ''):
    """
    读取配置文件中的值，如果配置项不存在则返回默认值
    :param config:
    :param key_path:
    :param default_value:
    :return:
    """
    keys = key_path.split(".")
    current = config
    for key in keys:
        if isinstance(current, dict):
            if key in current:
                current = current[key]
                if isinstance(current, str):
                    return current
            else:
                return default_value
        else:
            return current
