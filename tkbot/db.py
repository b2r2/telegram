import sqlite3
import logging


class Log():
    def __init__(self, path_log, path_copy_log):
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

        copy_filehandler = logging.FileHandler(path_copy_log)
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
    def __init__(self, path_db, path_log, path_copy_log):
        self.log = Log(path_log, path_copy_log)

        self.connection = sqlite3.connect(path_db,
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

# DEBUG#######################################

    def show_Database(self):
        sql = "SELECT * FROM ADV_USERS"
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.show_Database.__name__)
        else:
            self.log.info(self.show_Database.__name__)
            return self.cursor.fetchall()

###############################################
# INSERT OR UPDATE METHODS ####################
###############################################
    def insert_Into_Database(self, user_id):
        """ Insert database """
        sql = "INSERT OR IGNORE INTO ADV_USERS(USER_ID) VALUES(?)"
        try:
            self.cursor.execute(sql, (user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.insert_Into_Database.__name__)
        else:
            self.log.info(self.insert_Into_Database.__name__)
###############################################

    def update_Adv_Message_User(self, user_id, message, date):
        """ Insert or Update advertising message """
        self.insert_Into_Database(user_id)
        sql = "UPDATE ADV_USERS SET MESSAGE=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (message, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.update_Adv_Message_User.__name__)
        else:
            self.log.info(self.update_Adv_Message_User.__name__)

    def update_Channel_User(self, user_id, channel, date):
        """ Insert or Update channel name """
        self.insert_Into_Database(user_id)
        sql = "UPDATE ADV_USERS SET CHANNEL=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (channel, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.update_Channel_User.__name__)
        else:
            self.log.info(self.update_Channel_User.__name__)

    def update_Schedule_User(self, user_id, sched, date):
        """ Insert or Update schedule """
        self.insert_Into_Database(user_id)
        sql = "UPDATE ADV_USERS SET SCHEDULE=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (sched, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.update_Schedule_User.__name__)
        else:
            self.log.info(self.update_Schedule_User.__name__)

###############################################
# RETURN METHODS ##############################
###############################################

    def return_Adv_Message_User(self, user_id):
        """ Return advertising message """
        sql = "SELECT MESSAGE FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.return_Adv_Message_User.__name__)
        else:
            self.log.info(self.return_Adv_Message_User.__name__)
            return self.cursor.fetchall()

    def return_Channel_User(self, user_id):
        """ Return Channel name """
        sql = "SELECT CHANNEL FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.return_Channel_User.__name__)
        else:
            self.log.info(self.return_Channel_User.__name__)
            return self.cursor.fetchall()

    def return_Schedule_User(self, user_id):
        """ Return schedule """
        sql = "SELECT SCHEDULE FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.return_Schedule_User.__name__)
        else:
            self.log.info(self.return_Schedule_User.__name__)
            return self.cursor.fetchall()

    def return_All_Database_User(self, user_id):
        """ Return all the data about the user """
        sql = "SELECT * FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            self.log.error(err, self.return_All_Database_User.__name__)
        else:
            self.log.info(self.return_All_Database_User.__name__)
            return self.cursor.fetchall()
