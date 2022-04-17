import logging
import sys

logger = logging.getLogger('user_logger')

logger_format = logging.Formatter(
    '%(asctime)s.%(msecs)03d [%(levelname)s]|[%(name)s]: %(message)s'
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(logger_format)
stream_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)
