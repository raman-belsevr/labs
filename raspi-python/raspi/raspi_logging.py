import logging


def get_logger(name):

    logger = logging.getLogger("belsevr." + name)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler('belsevr_node.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(name)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)

    return logger