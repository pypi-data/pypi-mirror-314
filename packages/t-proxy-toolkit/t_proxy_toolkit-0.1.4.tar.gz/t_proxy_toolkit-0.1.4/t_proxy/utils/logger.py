"""Logger."""
import logging

log_format = logging.Formatter(
    r"%(asctime)s - %(levelname)-7s %(threadName)-12s [%(filename)s:%(lineno)s - %(funcName)s()] - %(message)s"
)
log_level = logging.DEBUG

logger = logging.getLogger("t_bug_catcher")
if logger.hasHandlers():
    logger.handlers = []
logger.setLevel(log_level)
logger.propagate = False

handler = logging.StreamHandler()
handler.setLevel(log_level)
handler.setFormatter(log_format)
logger.addHandler(handler)
