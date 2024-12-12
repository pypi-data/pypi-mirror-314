import logging
from logging.handlers import TimedRotatingFileHandler
import pyqqq.config as c
import sys

_format = "%(levelname).1s %(name)s: %(message)s"

if not c.is_google_cloud_logging_enabled():
    _format = "%(asctime)s " + _format

_stdout_h = logging.StreamHandler(sys.stdout)
_stdout_h.setLevel(logging.DEBUG)
_stdout_h.addFilter(lambda r: r.levelno <= logging.WARNING)

_stderr_h = logging.StreamHandler(sys.stderr)
_stderr_h.setLevel(logging.ERROR)

logging.basicConfig(format=_format, handlers=[_stdout_h, _stderr_h])


def get_logger(
        name,
        level=logging.DEBUG,
        filename: str = None,
        when: str = 'h',
        interval: int = 1,
        backup_count: int = 24,
) -> logging.Logger:
    """
    로깅을 위한 Logger 객체를 구성하고 반환합니다.

    이 함수는 주어진 이름과 세부 사항으로 Logger를 생성하고 설정합니다. 로그 파일 출력이 필요한 경우,
    파일 이름과 로테이션 정책(시간 간격 및 백업 수)을 지정할 수 있습니다. 로그는 지정된 레벨 또는 그 이상의 메시지만 기록합니다.

    Args:
        name (str): Logger의 이름.
        level (int, optional): 로깅 레벨. 기본값은 logging.DEBUG.
        filename (str, optional): 로그 파일의 이름. 지정하지 않으면 콘솔 로깅만 수행됩니다.
        when (str, optional): 로그 파일의 로테이션 주기 단위. 기본값은 'h'(시간).
        interval (int, optional): 로테이션 간격. 'when'에 지정된 단위에 따라 계산됩니다. 기본값은 1.
        backup_count (int, optional): 보관할 백업 파일의 최대 개수. 기본값은 24.

    Returns:
        logging.Logger: 구성된 로거 객체.

    Examples:
        >>> logger = get_logger('my_logger', filename='myapp.log')
        >>> logger.info('This is an info message')
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers and filename:
        fh = TimedRotatingFileHandler(
            filename, when=when, backupCount=backup_count, interval=interval
        )
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter(_format))
        logger.addHandler(fh)

    return logger


def set_all_logger_level(level):
    """
    모든 로거의 로깅 레벨을 하나로 맞춘다.
    """
    if level not in [
        logging.CRITICAL,
        logging.ERROR,
        logging.WARNING,
        logging.INFO,
        logging.DEBUG,
    ]:
        raise ValueError("Invalid log level")

    for logger_name in logging.root.manager.loggerDict:
        logging.getLogger(logger_name).setLevel(level)
