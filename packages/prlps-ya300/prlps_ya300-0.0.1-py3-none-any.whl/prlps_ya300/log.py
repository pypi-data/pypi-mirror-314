from logging import CRITICAL, DEBUG, ERROR, Formatter, INFO, Logger, StreamHandler, WARNING, getLogger
from typing import Literal

LogLevels = Literal['crit', 'critical', 'err', 'error', 'warn', 'warning', 'info', 'debug']

def str_to_bool(value: str) -> bool:
    return str(value).strip().lower() in {'true', '1', 'yes', 'y'}


def str_to_log_level(value: str) -> int:
    return {'crit': CRITICAL, 'critical': CRITICAL, 'err': ERROR, 'error': ERROR,
            'warn': WARNING, 'warning': WARNING, 'info': INFO, 'debug': DEBUG
            }.get(value.strip().lower(), WARNING)


def set_logging(level: str = LogLevels, name: str = 'YA-300') -> Logger:
    """
    настраивает логирование для приложения в консоли.

    Args:
        level (str): устанавливает уровень логирования, по умолчанию 'WARNING'.
        name (str): имя логгера, по умолчанию 'YA-300'.

    Returns:
        logging.Logger: настроенный экземпляры класса Logger
    """
    log_lvl = str_to_log_level(level)
    app_logger = getLogger(name)
    app_logger.setLevel(log_lvl)
    handler = StreamHandler()
    handler.setLevel(log_lvl)
    handler.setFormatter(Formatter('[%(name)s]:%(levelname)s - %(message)s'))
    app_logger.addHandler(handler)
    app_logger.propagate = False
    return app_logger
