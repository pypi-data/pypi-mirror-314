import os
import logging
from logging.handlers import TimedRotatingFileHandler
from .util.common import load_config, config_value


def load_log_config():
    """
    从环境变量中加载日志配置信息
    :return:
    """
    config = load_config()
    log_level = config_value(config, 'log.level', 'INFO')
    log_dir = config_value(config, 'log.dir', '/tmp/logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_level, log_dir


def format_log():
    """
    设置日志输出格式
    :return:
    """
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')
    return formatter


def logger_instance(name):
    """
    生成日志实例
    :param name: 日志实例名称
    :return: Logger
    """
    # 载入日志配置信息
    log_level, log_dir = load_log_config()
    instance = logging.getLogger(name)
    instance.setLevel(log_level)
    # 控制台日志处理
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(format_log())
    instance.addHandler(console_handler)
    # 文件日志处理
    file_handler = TimedRotatingFileHandler(f'{log_dir}/app.log', when='midnight', interval=1)
    file_handler.setFormatter(format_log())
    file_handler.suffix = '%Y%m%d'
    instance.addHandler(file_handler)
    return instance
