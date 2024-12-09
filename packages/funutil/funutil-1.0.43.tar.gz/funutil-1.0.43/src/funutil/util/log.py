import logging
import os
import sys
from functools import cache

from loguru import logger

if not os.path.exists("logs"):
    os.makedirs("logs", exist_ok=True)
    with open("logs/.gitignore", "w") as f:
        f.write("*")

logger.configure(
    handlers=[
        {
            "sink": sys.stderr,
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} |<lvl>{level:8}</>| {name} : {module}:{line:4} | <cyan>{extra[module_name]}</> | - <lvl>{message}</>",
            "colorize": True,
        },
        {
            "sink": "logs/all.log",
            "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} |{level:8}| {name} : {module}:{line:4} | {extra[module_name]} | - {message}",
            "colorize": False,
            "rotation": "00:00",
            "compression": "gz",
            "retention": 30,
        },
    ]
)


@cache
def _get_logger_bak(name="default", level=logging.INFO, formatter=None, handler=None):
    formatter = (
        formatter
        or "%(asctime)s %(name)s %(levelname)s [%(filename)s - %(lineno)d - %(funcName)s] %(message)s"
    )
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        logger.info(f"logger={name} is already configured")
        return logger
    if handler is None:
        handler = logging.StreamHandler()
        handler.setLevel(level=level)
        handler.setFormatter(logging.Formatter(formatter))
    logger.addHandler(handler)
    logger.setLevel(level=level)

    logger.info(
        f"init logger with name={name} and level={logging.getLevelName(level)}",
    )
    return logger


def _getLoggerBak(
    name="default",
    level=logging.INFO,
    formatter=None,
    handler=None,
):
    return _get_logger_bak(name, level=level, formatter=formatter, handler=handler)


@cache
def get_logger(name="default", level="DEBUG", formatter=None, *args, **kwargs):
    if not os.path.exists("logs"):
        os.makedirs("logs", exist_ok=True)
        with open("logs/.gitignore", "w") as f:
            f.write("*")
    logger.add(
        sink=f"logs/{name}.log",
        format=formatter
        or "{time:YYYY-MM-DD HH:mm:ss.SSS} |{level:8}| {name} : {module}:{line:4} | {extra[module_name]} | - {message}",
        filter=lambda record: record["extra"].get("module_name") == name,
        level=level,
        rotation="00:00",
        compression="gz",
        retention=7,
        colorize=False,
    )
    return logger.bind(module_name=name)


def getLogger(
    name="default", level="DEBUG", formatter=None, handler=None, *args, **kwargs
):
    return get_logger(name, level=level, formatter=formatter, handler=handler)
