import logging

def get_logger(log_file_path='/var/log/coconut_news/backend.log'):
    logger = logging.getLogger('coconut_news')
    handler = logging.FileHandler(log_file_path)
    formatter = logging.Formatter('%(levelname)s %(message)s %(asctime)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # Do not set log level, we want all the logs.
    return logger
