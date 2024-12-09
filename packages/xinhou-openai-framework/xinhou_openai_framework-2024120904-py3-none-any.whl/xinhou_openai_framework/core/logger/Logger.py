import logging
import colorlog


class Logger:
    """
    Logger类，提供带有额外信息支持的彩色日志输出。

    属性:
        DEBUG (int): 调试级别的日志记录。
        INFO (int): 信息级别的日志记录。
        WARNING (int): 警告级别的日志记录。
        ERROR (int): 错误级别的日志记录。
        CRITICAL (int): 严重级别的日志记录。
    """

    # 定义日志级别常量
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    def __init__(self, name=__name__, level=INFO):
        """
        初始化Logger实例。

        参数:
            name (str): 日志记录器的名称。默认为模块的__name__。
            level (int): 日志记录的级别。默认为INFO。
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(Logger.colored_formatter())
        self.logger.addHandler(console_handler)

    def info(self, msg, *args, **kwargs):
        """
        记录INFO级别的日志信息。

        参数:
            msg (str): 日志信息。
            *args: 可变参数。
            **kwargs: 关键字参数。
        """
        extra_info = kwargs.pop('extra_info', None)
        if extra_info is not None:
            msg += f" Extra Info: {extra_info}"
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """
        记录DEBUG级别的日志信息。

        参数:
            msg (str): 日志信息。
            *args: 可变参数。
            **kwargs: 关键字参数。
        """
        extra_info = kwargs.pop('extra_info', None)
        if extra_info is not None:
            msg += f" Extra Info: {extra_info}"
        self.logger.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        记录WARNING级别的日志信息。

        参数:
            msg (str): 日志信息。
            *args: 可变参数。
            **kwargs: 关键字参数。
        """
        extra_info = kwargs.pop('extra_info', None)
        if extra_info is not None:
            msg += f" Extra Info: {extra_info}"
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """
        记录ERROR级别的日志信息。

        参数:
            msg (str): 日志信息。
            *args: 可变参数。
            **kwargs: 关键字参数。
        """
        extra_info = kwargs.pop('extra_info', None)
        if extra_info is not None:
            msg += f" Extra Info: {extra_info}"
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """
        记录CRITICAL级别的日志信息。

        参数:
            msg (str): 日志信息。
            *args: 可变参数。
            **kwargs: 关键字参数。
        """
        extra_info = kwargs.pop('extra_info', None)
        if extra_info is not None:
            msg += f" Extra Info: {extra_info}"
        self.logger.critical(msg, *args, **kwargs)

    @staticmethod
    def colored_formatter():
        """
        创建并返回一个彩色日志格式化器。

        返回:
            colorlog.ColoredFormatter: 带有颜色设置的日志格式化器。
        """
        return colorlog.ColoredFormatter(
            '%(asctime)s | %(log_color)s%(levelname)-4s%(reset)s | %(name)-10s:%(funcName)-8s:(%(lineno)d) | %(message)s',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )


# 测试Logger类
if __name__ == '__main__':
    logger = Logger("my_logger", Logger.DEBUG)

    logger.info("This is an info msg.")
    logger.debug("This is a debug msg.")
    logger.warning("This is a warning msg with additional info:", extra_info="extra info")
    logger.error("This is an error msg with additional info:", extra_info="error details")
    logger.critical("This is a critical msg with additional info:", extra_info="critical details")
