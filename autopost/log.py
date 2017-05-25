# -*- coding: utf-8 -*-


import logging
import settings


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='%(levelname)s:%(name)s: %(message)s'
                              ' (%(asctime)s: line: %(lineno)d)',
                              datefmt='%Y-%m-%d %H:%M:%S')

console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)

filehandler = logging.FileHandler(settings.logs_path)
filehandler.setFormatter(formatter)
filehandler.setLevel(logging.ERROR)

copy_filehandler = logging.FileHandler(settings.copy_logs_path)
copy_filehandler.setFormatter(formatter)
copy_filehandler.setLevel(logging.ERROR)

logger.addHandler(console)
logger.addHandler(filehandler)
logger.addHandler(copy_filehandler)


def log_err(msg):
    logger.exception('Message error:%-10%' % msg.upper())


def log_info(msg):
    logger.info('Start handler: %-10s' % msg.upper())
    logger.info('Successful:    %-10s' % msg.upper())
