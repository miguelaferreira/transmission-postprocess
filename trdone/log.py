import logging


def init_logger(name):
    log_format = '[%(levelname)s] %(asctime)s - %(name)s - %(message)s'
    logger = logging.getLogger(name)
    if len(logger.handlers) == 0:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(log_format))
        ch.setLevel(logging.INFO)
        logger.addHandler(ch)
        logger.setLevel(logging.INFO)
    return logger
