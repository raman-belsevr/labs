import logging


def get_logger(name):

    logger = logging.getLogger("belsevr." + name)
    logger.setLevel(logging.INFO)
    # create a file handler
    handler = logging.FileHandler('belsevr_node.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(handler)
    return logging.getLogger(__name__)