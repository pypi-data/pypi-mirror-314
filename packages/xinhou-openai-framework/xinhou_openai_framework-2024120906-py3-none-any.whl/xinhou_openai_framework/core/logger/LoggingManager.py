import logging
import os
import sys
from datetime import datetime
from logging import StreamHandler
from logging.handlers import RotatingFileHandler

from loguru import logger as loguru_logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # 获取对应的 Loguru 级别
        try:
            level = loguru_logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 找到调用者的文件名和行号
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru_logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


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

        # 移除所有已存在的处理器
        loguru_logger.remove()
        
        # 配置 loguru
        config = {
            "handlers": [
                {
                    "sink": sys.stdout,
                    "format": "<green>{time:YYYY-MM-DD HH:mm:ss,SSS}</green> | <level>{level: <8}</level> | <cyan>{name}:{function}:{line}</cyan> | <level>{message}</level>",
                    "colorize": True,
                    "level": "INFO"
                },
                {
                    "sink": file_info,
                    "format": "{time:YYYY-MM-DD HH:mm:ss,SSS} | {level: <8} | {name}:{function}:{line} | {message}",
                    "rotation": "00:00",
                    "retention": "7 days",
                    "compression": "zip",
                    "level": "INFO"
                }
            ]
        }

        # 应用 loguru 配置
        for handler in config["handlers"]:
            loguru_logger.add(**handler)

        # 替换所有标准库的处理器
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

        # 替换 uvicorn 的日志配置
        for _log in ['uvicorn', 'uvicorn.error', 'uvicorn.access', 'sqlalchemy.engine']:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]
            _logger.propagate = False

        # 初始化其他模块的日志处理器
        LoggingManager.init_custom_logger('sqlalchemy', file_info)
        LoggingManager.init_custom_logger('nacos', file_info)
        LoggingManager.init_custom_logger('skywalking', file_info)

    @staticmethod
    def init_custom_logger(name, file_info):
        """
        为特定模块初始化日志处理器
        """
        custom_logger = logging.getLogger(name)
        custom_logger.handlers = [InterceptHandler()]
        custom_logger.propagate = False
