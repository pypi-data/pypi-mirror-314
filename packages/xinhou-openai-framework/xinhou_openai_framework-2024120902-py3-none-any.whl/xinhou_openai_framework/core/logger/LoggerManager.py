import logging
import os
from datetime import datetime
from logging import StreamHandler
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from loguru import logger as loguru_logger


class LoggerManager:

    @staticmethod
    def init_logger(app, log_path: str = None):
        """
        初始化 logger，将日志同时输出到 console 和指定的文件中。
        """
        if log_path is None:
            return

        # 确保日志目录存在
        os.makedirs(log_path, exist_ok=True)

        # 生成基础日志文件路径
        base_file_info = os.path.join(log_path, "app.log")

        # 移除 loguru 默认的处理器
        loguru_logger.remove()

        # 添加控制台处理器
        loguru_logger.add(
            sink=StreamHandler(),
            format="<green>{time:YYYY-MM-DD HH:mm:ss,SSS}</green> | <level>{level: <8}</level> | <cyan>{name}:{function}:{line}</cyan> | <level>{message}</level>",
            colorize=True,
            enqueue=True,
            level="INFO"
        )

        # 添加文件处理器
        loguru_logger.add(
            sink=base_file_info,
            format="{time:YYYY-MM-DD HH:mm:ss,SSS} | {level} | {name}:{function}:{line} | {message}",
            rotation="00:00",  # 每天午夜轮转
            retention="7 days",  # 保留7天
            encoding="utf-8",
            compression="zip",
            level="INFO",
            enqueue=True,
            # 自定义轮转后的文件名格式
            rotation_format='{time:YYYY-MM-DD}.log'
        )

        # 初始化其他模块的日志处理器
        LoggerManager.init_custom_logger('sqlalchemy', log_path)
        LoggerManager.init_custom_logger('nacos', log_path)
        LoggerManager.init_custom_logger('skywalking', log_path)

    @staticmethod
    def init_custom_logger(name, log_path):
        custom_logger = logging.getLogger(name)
        if not custom_logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d | %(message)s')

            # 使用 TimedRotatingFileHandler 进行按日期轮转
            file_handler = TimedRotatingFileHandler(
                filename=os.path.join(log_path, f"{name}.log"),
                when='midnight',  # 每天午夜轮转
                interval=1,  # 间隔为1天
                backupCount=7,  # 保留7天的日志
                encoding='utf-8'
            )
            # 设置轮转后的文件名格式
            file_handler.suffix = "%Y-%m-%d"
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)
            custom_logger.addHandler(file_handler)

            # 添加控制台处理器
            console_handler = StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            custom_logger.addHandler(console_handler)
