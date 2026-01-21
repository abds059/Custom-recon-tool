import logging
import sys


def get_logger(verbosity: int = 0) -> logging.Logger:
    logger = logging.getLogger("recon-tool")

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "[%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger
