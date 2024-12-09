# encoding:utf-8
import logging

class LogLevel:
    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10


class _MyLogger(logging.Logger):
    def __init__(self, name, level=logging.INFO):
        self.addHandler(console_handler)
        pass


log_ld = _MyLogger("零动插件", logging.ERROR)
log = _MyLogger("日志", logging.DEBUG)

__all__ = ['log_ld', 'log', "LogLevel"]
