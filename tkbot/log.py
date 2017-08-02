import logging


class Log():
    def __init__(self, path):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt='%(levelname)s:%(name)s# %(message)s'
                                      '# (%(asctime)s)',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)

        filehandler = logging.FileHandler(path.log)
        filehandler.setFormatter(formatter)
        filehandler.setLevel(logging.ERROR)

        copy_filehandler = logging.FileHandler(path.clog)
        copy_filehandler.setFormatter(formatter)
        copy_filehandler.setLevel(logging.ERROR)

        self.logger.addHandler(console)
        self.logger.addHandler(filehandler)
        self.logger.addHandler(copy_filehandler)

    def error(self, err, method_name):
        self.logger.exception(' Error type: %s. Method: %s', err, method_name)

    def info(self, method_name):
        self.logger.info(' %s: success', method_name)
