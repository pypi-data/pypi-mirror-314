import logging
import os.path
import time

from P_EO.common.config import LogConfig

__all__ = ['set_logger', 'LogMixin']

LOGGER: logging.Logger = None


def default_log() -> logging.Logger:
    _logger = logging.getLogger('PEO')
    _logger.setLevel(logging.DEBUG)
    default_log_format = "%(asctime)s-[%(filename)s:%(lineno)d]-[%(levelname)s]: %(message)s"
    default_log_path = os.path.join(os.getcwd(), 'peo_log', time.strftime("%Y%m%d"))
    default_log_name = f'peo_error.log'

    if LogConfig.STREAM:
        stream = logging.StreamHandler()
        _format = LogConfig.STREAM_FORMAT if LogConfig.STREAM_FORMAT else default_log_format
        formatter = logging.Formatter(fmt=_format)
        stream.setFormatter(formatter)
        stream.setLevel(LogConfig.STREAM_LEVEL)
        _logger.addHandler(stream)

    if LogConfig.LOG_FILE or LogConfig.SAVE_ERROR:
        if LogConfig.LOG_FILE:
            _path = LogConfig.LOG_FILE
        else:
            os.makedirs(default_log_path, exist_ok=True)
            _path = os.path.join(default_log_path, default_log_name)
            LogConfig.LOG_FILE_LEVEL = logging.ERROR

        file = logging.FileHandler(_path)
        _format = LogConfig.LOG_FILE_FORMAT if LogConfig.LOG_FILE_FORMAT else default_log_format
        formatter = logging.Formatter(fmt=_format)
        file.setFormatter(formatter)
        file.setLevel(LogConfig.LOG_FILE_LEVEL)
        _logger.addHandler(file)

    return _logger


def set_logger(logger: logging.Logger):
    if not isinstance(logger, logging.Logger):
        raise Exception(f'logger 类型不正确！{logger}')

    global LOGGER
    LOGGER = LOGGER


class LogMixin:
    @staticmethod
    def init_log():
        global LOGGER
        if LOGGER is None:
            LOGGER = default_log()

    @property
    def log(self) -> logging.Logger:
        self.init_log()
        return LOGGER
