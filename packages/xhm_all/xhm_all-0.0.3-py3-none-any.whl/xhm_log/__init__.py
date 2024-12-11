import json
import logging
import os
import socket
import time
import uuid
from datetime import datetime
from enum import Enum
from logging.handlers import TimedRotatingFileHandler
from xhm_config import conf
import inspect

# 禁用外部库日志
logging.getLogger("root").setLevel(logging.INFO)
logging.getLogger("elasticsearch").setLevel(logging.WARNING)
logging.getLogger("pulsar").setLevel(logging.WARNING)
logging.getLogger("peewee").setLevel(logging.WARNING)
logging.getLogger("qcloud_cos").setLevel(logging.WARNING)


class LogColors(Enum):
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def _basic_config() -> logging.Logger:
    """Configure basic logging settings with daily log file rotation."""
    service_name = conf.get("service_name")
    log_level = conf.get("log_level")

    # 设置日志文件路径为 logs 目录下
    logs_folder = "logs"
    os.makedirs(logs_folder, exist_ok=True)  # 如果 logs 文件夹不存在，则创建它
    hostname = socket.gethostname()  # 获取容器的 hostname
    log_filename = os.path.join(logs_folder, f'{service_name.replace(" ", "_")}_{hostname}.log')
    # 获取 root logger
    root_logger = logging.getLogger(service_name)

    # 确保 root logger 没有重复的 handlers
    if root_logger.hasHandlers():
        root_logger.handlers.clear()  # 清除所有已有的 handlers，避免重复

    # Create a TimedRotatingFileHandler that rotates the log file every midnight
    handler = TimedRotatingFileHandler(
        log_filename, when='midnight', interval=1, backupCount=7
    )
    handler.suffix = "%Y-%m-%d.log"  # Log file name will include the date (e.g., logfile-2024-11-22.log)

    class JsonFormatter(logging.Formatter):
        def format(self, record):
            # Get the log message and additional metadata as JSON
            log_message = record.getMessage()
            log_data = {
                "timestamp": int(time.time() * 1000),
                "level": record.levelname,
                "message": log_message,
                "file": record.pathname,
                "line": record.lineno,
                "service": conf.get("service_name"),
                "host": socket.gethostname(),
                "event_type": getattr(record, 'event_type', ''),
                "event_data": getattr(record, 'event_data', {}),
                "x_request_id": getattr(record, 'x_request_id', None) or str(uuid.uuid4()),
            }
            return json.dumps(log_data, ensure_ascii=False)

    handler.setFormatter(JsonFormatter())

    # 非json
    # handler.setFormatter(logging.Formatter(
    #     "[%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

    # Set up logger
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)
    return root_logger


bclog = _basic_config()


def _log_message(log_func, color: LogColors, message: str, event_type: str = "", event_data: dict = None,
                 x_request_id: str = ""):
    """Helper function to log messages with color, using stacklevel to adjust the line number shown."""

    # Dynamically get the caller's information for accurate line numbers
    if event_data is None:
        event_data = {}
    caller_frame = inspect.stack()[2]
    caller_filename = caller_frame.filename
    caller_line = caller_frame.lineno
    log_level = color.value + LogColors.BOLD.value + log_func.__name__.upper() + LogColors.ENDC.value
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # 截取到毫秒

    colored_message = color.value + LogColors.BOLD.value + message + LogColors.ENDC.value

    extra = {"event_type": event_type, "event_data": event_data, "x_request_id": x_request_id}

    # For console log:
    log_func(message, stacklevel=3, extra=extra)  # Adjusting stacklevel to get correct line number
    print(f"{log_time} | {log_level} | {caller_filename}:{caller_line} - " + colored_message)


def warning(s: str, event_type: str = "", event_data: dict = None, x_request_id: str = ""):
    """Log warning level messages."""
    _log_message(bclog.warning, LogColors.WARNING, s,
                 event_type, event_data, x_request_id)


def info(s: str, event_type: str = "", event_data: dict = None, x_request_id: str = ""):
    """Log info level messages."""
    _log_message(bclog.info, LogColors.OKGREEN, s,
                 event_type, event_data, x_request_id)


def error(s: str, event_type: str = "", event_data: dict = None, x_request_id: str = ""):
    """Log error level messages."""
    _log_message(bclog.error, LogColors.FAIL, s,
                 event_type, event_data, x_request_id)


def debug(s: str, event_type: str = "", event_data: dict = None, x_request_id: str = ""):
    """Log error level messages."""
    _log_message(bclog.debug, LogColors.OKCYAN, s,
                 event_type, event_data, x_request_id)


def critical(s: str, event_type: str = "", event_data: dict = None, x_request_id: str = ""):
    """Log error level messages."""
    _log_message(bclog.critical, LogColors.HEADER, s,
                 event_type, event_data, x_request_id)
