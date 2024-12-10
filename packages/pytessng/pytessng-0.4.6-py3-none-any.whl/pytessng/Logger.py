import os
import logging
from datetime import datetime

from pytessng.Config import LoggingConfig, PathConfig


class Logger:
    def __init__(self):
        self.logger_pytessng = self.setup_logger("pytessng")

    @staticmethod
    def setup_logger(name, file_level=LoggingConfig.FILE_LOGS_LEVEL, console_level=LoggingConfig.CONSOLE_LOGS_LEVEL):
        save_log_path = PathConfig.LOG_DIR_PATH
        # 确保文件夹存在
        os.makedirs(save_log_path, exist_ok=True)
        # 保存路径
        current_date = datetime.now().strftime('%Y%m%d')
        save_log_file_path = f"{save_log_path}\\{name}_{current_date}.log"

        # 创建日志记录器对象
        logger = logging.getLogger(name)

        # 清空已存在的处理程序和过滤器，以防止重复添加
        logger.handlers = []
        logger.filters = []

        # 创建一个文件处理程序
        file_handler = logging.FileHandler(save_log_file_path, encoding='utf-8')  # 输出到文件
        # 创建一个控制台处理程序
        console_handler = logging.StreamHandler()  # 输出到控制台

        # 创建一个格式化器，定义日志信息格式
        format_string = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        file_formatter = logging.Formatter(format_string)
        console_formatter = ColoredFormatter(format_string)

        # 设置日志级别
        file_handler.setLevel(file_level)
        console_handler.setLevel(console_level)

        # 设置格式化器
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # 将文件处理程序和控制台处理程序添加到日志记录器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # 设置记录器的级别
        logger.setLevel(logging.DEBUG)

        return logger


class ColoredFormatter(logging.Formatter):
    # 定义颜色代码
    COLORS = {
        'DEBUG': '\033[94m',  # 蓝色
        'INFO': '\033[92m',  # 绿色
        'WARNING': '\033[93m',  # 橙色
        'ERROR': '\033[91m',  # 红色
        'CRITICAL': '\033[95m'  # 紫色
    }
    RESET = '\033[0m'

    def format(self, record):
        # 在格式化消息时应用颜色
        color = self.COLORS.get(record.levelname, self.RESET)
        message = super().format(record)
        return f'{color}{message}{self.RESET}'


# 全局日志记录器
logger = Logger()
