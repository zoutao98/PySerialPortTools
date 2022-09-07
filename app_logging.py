import logging

def getLogger(name) -> logging.Logger:

    log = logging.getLogger(name)
    LOG_FORMAT = "%(asctime)s %(threadName)s:" + logging.BASIC_FORMAT
    log.setLevel(logging.INFO)

    file_handler = logging.FileHandler('app.log', 'a', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    log.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    log.addHandler(console_handler)

    return log