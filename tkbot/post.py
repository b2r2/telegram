import db
import logging


class Log():
    def __init__(self, path_log, path_clog):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(fmt='%(levelname)s:%(name)s# %(message)s'
                                      '# (%(asctime)s)',
                                      datefmt='%Y-%m-%d %H:%M:%S')

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)

        filehandler = logging.FileHandler(path_log)
        filehandler.setFormatter(formatter)
        filehandler.setLevel(logging.ERROR)

        copy_filehandler = logging.FileHandler(path_clog)
        copy_filehandler.setFormatter(formatter)
        copy_filehandler.setLevel(logging.ERROR)

        self.logger.addHandler(console)
        self.logger.addHandler(filehandler)
        self.logger.addHandler(copy_filehandler)

    def error(self, function_name, msg):
        self.logger.exception('Error:  %s. Sending a file(type %s)',
                              function_name, msg)

    def info(self, function_name):
        self.logger.info('%s: success', function_name)


class Post():
    def __init__(self, user_id, database, path_log, path_clog):
        self.log = Log(path_log, path_clog)
        self.db = database
        self.user_id = user_id

    def make_post(self):
        self.post = {}
        try:
            self.post['message'] = db.returnAdvMessage(self.user_id)
            self.post['channel'] = db.returnChannelMessage(self.user_id)
        except Exception as err:
            self.log.error(err, self.make_post.__name__)
        else:
            return self.post
