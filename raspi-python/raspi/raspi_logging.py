import logging

app_logger = None


def get_logger(name):
    global app_logger
    if app_logger is None:
        app_logger = build_logger(name)
    else:
    return app_logger


def build_logger(name):
    logger = logging.getLogger("belsevr." + name)
    logger.setLevel(logging.INFO)

    # create a file handler
    handler = logging.FileHandler('belsevr_node.log')
    handler.setLevel(logging.INFO)

    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(name)s')
    handler.setFormatter(formatter)

    # add the handlers to the logger
    # print("built logger [{}]".format(name))
    logger.addHandler(handler)

    return logger