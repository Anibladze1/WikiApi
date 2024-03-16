import logging


def get_logger(name, level=logging.INFO):
    """
    Creates and returns a logger instance with the specified name and level.

    The logger is configured with a file handler that writes logs to 'app.log'.
    It uses a standard logging format that includes the timestamp, logger name,
    log level, and log message. If the logger already has handlers, it does not
    add another, preventing duplicate logging.

    :param name: The name of the logger, typically the module's __name__.
                 This helps to identify where the log entry originated.
    :param level: The logging level, e.g., logging.INFO, logging.DEBUG, etc.
                  This determines the severity of messages the logger will handle.
    :return: A configured logging.Logger instance that writes to 'app.log' and
             uses the specified logging level.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.FileHandler('app.log')
    handler.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger
