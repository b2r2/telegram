import sqlite3
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

    def error(self, function_name, msg):
        self.logger.exception('Error:  %s. Sending a file(type %s)',
                              function_name, msg)

    def info(self, function_name):
        self.logger.info('%s: success', function_name)


class Database():
    def __init__(self, path):
        self.log = Log(path)

        self.connection = sqlite3.connect(path.db,
                                          check_same_thread=False)
        self.cursor = self.connection.cursor()
        sql = """ CREATE TABLE IF NOT EXISTS ADV_USERS
              (ID INTEGER PRIMARY KEY AUTOINCREMENT,
              USER_ID INTEGER UNIQUE,
              CHANNEL TEXT,
              MESSAGE TEXT,
              SCHEDULE TEXT,
              DATE INTEGER) """
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.__init__.__name__)
        else:
            self.log.info(self.__init__.__name__)

    def add_field(self, user_id):
        """ Insert database """
        sql = "INSERT OR IGNORE INTO ADV_USERS(USER_ID) VALUES(?)"
        try:
            self.cursor.execute(sql, (user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.add_field.__name__)
        else:
            self.log.info(self.add_field.__name__)

    def update_adv_message(self, user_id, message, date):
        """ Insert or Update advertising message """
        self.add_field(user_id)
        sql = "UPDATE ADV_USERS SET MESSAGE=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (message, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.update_adv_message.__name__)
        else:
            self.log.info(self.update_adv_message.__name__)

    def update_channel_message(self, user_id, channel, date):
        """ Insert or Update channel name """
        self.add_field(user_id)
        sql = "UPDATE ADV_USERS SET CHANNEL=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (channel, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.update_channel_message.__name__)
        else:
            self.log.info(self.update_channel_message.__name__)

    def update_schedule_message(self, user_id, sched, date):
        """ Insert or Update schedule """
        self.add_field(user_id)
        sql = "UPDATE ADV_USERS SET SCHEDULE=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (sched, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.update_schedule_message.__name__)
        else:
            self.log.info(self.update_schedule_message.__name__)

    def return_field(self, user_id, sort):
        if sort == 'advertising':
            sql = "SELECT MESSAGE FROM ADV_USERS WHERE USER_ID=?"
        elif sort == 'channel':
            sql = "SELECT CHANNEL FROM ADV_USERS WHERE USER_ID=?"
        elif sort == 'schedule':
            sql = "SELECT SCHEDULE FROM ADV_USERS WHERE USER_ID=?"
        elif sort == 'mydata':
            sql = "SELECT CHANNEL,MESSAGE, SCHEDULE FROM ADV_USERS\
                WHERE USER_ID=?"
        else:
            sql = "SELECT * FROM ADV_USERS WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (user_id,))
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.return_field.__name__)
        else:
            self.log.info(self.return_field.__name__)
            return self.cursor.fetchall()
