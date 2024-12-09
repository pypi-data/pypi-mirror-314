import logging
import os
from datetime import datetime
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from loguru import logger as loguru_logger


class LoggingManager:

    @staticmethod
    def init_logger(app, log_path: str = None):
        """
        初始化 logger，将日志同时输出到 console 和指定的文件中。
        """
        if log_path is None:
            return

        # 确保日志目录存在
        os.makedirs(log_path, exist_ok=True)

        # 生成当天的日志文件路径
        file_info = os.path.join(log_path, f"{datetime.now().strftime('%Y-%m-%d')}.log")

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
            sink=file_info,
            format="{time:YYYY-MM-DD HH:mm:ss,SSS} | {level} | {name}:{function}:{line} | {message}",
            rotation="00:00",  # 每天轮转
            retention="7 days",  # 保留7天
            encoding="utf-8",
            compression="zip",
            level="INFO",
            enqueue=True
        )

        # 初始化其他模块的日志处理器
        LoggingManager.init_custom_logger('sqlalchemy', file_info)
        LoggingManager.init_custom_logger('nacos', file_info)
        LoggingManager.init_custom_logger('skywalking', file_info)

    @staticmethod
    def init_custom_logger(name, file_info):
        custom_logger = logging.getLogger(name)
        if not custom_logger.handlers:
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d | %(message)s')

            # 添加文件处理器
            custom_rf_handler = RotatingFileHandler(
                file_info,
                maxBytes=1000 * 1024 * 10,  # 10MB
                backupCount=10,
                encoding='utf-8'
            )
            custom_rf_handler.setLevel(logging.INFO)
            custom_rf_handler.setFormatter(formatter)
            custom_logger.addHandler(custom_rf_handler)

            # 添加控制台处理器
            console_handler = StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            custom_logger.addHandler(console_handler)
