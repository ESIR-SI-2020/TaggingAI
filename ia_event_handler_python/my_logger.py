import logging
from logging.handlers import RotatingFileHandler


def initLogger(ifFileLDebug, ifConsoleLDebug):
    
    # Setting the logging
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    logger.setLevel(logging.DEBUG)

    ## file logger handler
    file_handler = RotatingFileHandler('activity.log', 'a', 1000000, 1)
    if ifFileLDebug :
        file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    ## console logger handler
    stream_handler = logging.StreamHandler()
    if ifConsoleLDebug :
        stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    ## send warning in log for log level
    if ifConsoleLDebug :
        logger.warning('CONSOLE LOG DEBUG MODE ACTIVATED')

    if ifFileLDebug :
        logger.warning('FILE LOG DEBUG MODE ACTIVATED')

    logger.debug('Logger initialized')

    return logger