import sqlite3
import sys


sys.path.append('../')


import settings
import path
#########################################################################
# LOG CONFIG ############################################################
#########################################################################
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(fmt='%(levelname)s:%(name)s# %(message)s'
                              '# (%(asctime)s)',
                              datefmt='%Y-%m-%d %H:%M:%S')

console = logging.StreamHandler()
console.setFormatter(formatter)
console.setLevel(logging.INFO)

filehandler = logging.FileHandler(path.logs)
filehandler.setFormatter(formatter)
filehandler.setLevel(logging.ERROR)

copy_filehandler = logging.FileHandler(path.copy_logs)
copy_filehandler.setFormatter(formatter)
copy_filehandler.setLevel(logging.ERROR)

logger.addHandler(console)
logger.addHandler(filehandler)
logger.addHandler(copy_filehandler)

#########################################################################
#  FUNCTIONS ############################################################
#########################################################################


def log_Error(function_name, msg):
    logger.exception('Error:  %s. Sending a file(type %s)',
                     function_name, msg)


def log_Info(function_name):
    logger.info('%s: success', function_name)

##########################################################################


class Database():
    def __init__(self):
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
            log_Error(err, self.__init__.__name__)
        else:
            log_Info(self.__init__.__name__)

# DEBUG#######################################

    def show_Database(self):
        sql = "SELECT * FROM ADV_USERS"
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as err:
            log_Error(err, self.show_Database.__name__)
        else:
            log_Info(self.show_Database.__name__)
            return self.cursor.fetchall()

###############################################
# INSERT OR UPDATE METHODS ####################
###############################################
    def insert_Database(self, user_id):
        """ Insert database """
        sql = "INSERT OR IGNORE INTO ADV_USERS(USER_ID) VALUES(?)"
        try:
            self.cursor.execute(sql, (user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            log_Error(err, self.insert_Database.__name__)
        else:
            log_Info(self.insert_Database.__name__)

    def handler_Adv_Message_User(self, user_id, message, date):
        """ Insert or Update advertising message """
        self.insert_Database(user_id)
        sql = "UPDATE ADV_USERS SET MESSAGE=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (message, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            log_Error(err, self.handler_Adv_Message_User.__name__)
        else:
            log_Info(self.handler_Adv_Message_User.__name__)

    def handler_Channel_User(self, user_id, channel, date):
        """ Insert or Update channel name """
        self.insert_Database(user_id)
        sql = "UPDATE ADV_USERS SET CHANNEL=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (channel, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            log_Error(err, self.handler_Channel_User.__name__)
        else:
            log_Info(self.handler_Channel_User.__name__)

    def handle_Schedule_User(self, user_id, sched, date):
        """ Insert or Update schedule """
        self.insert_Database(user_id)
        sql = "UPDATE ADV_USERS SET SCHEDULE=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (sched, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            log_Error(err, self.handle_Schedule_User.__name__)
        else:
            log_Info(self.handle_Schedule_User.__name__)

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
            log_Error(err, self.return_Adv_Message_User.__name__)
        else:
            log_Info(self.return_Adv_Message_User.__name__)
            return self.cursor.fetchall()

    def return_Channel_User(self, user_id):
        """ Return Channel name """
        sql = "SELECT CHANNEL FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            log_Error(err, self.return_Channel_User.__name__)
        else:
            log_Info(self.return_Channel_User.__name__)
            return self.cursor.fetchall()

    def return_Schedule_User(self, user_id):
        """ Return schedule """
        sql = "SELECT SCHEDULE FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            log_Error(err, self.return_Schedule_User.__name__)
        else:
            log_Info(self.return_Schedule_User.__name__)
            return self.cursor.fetchall()

    def return_All_Database_User(self, user_id):
        """ Return all the data about the user """
        sql = "SELECT * FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            log_Error(err, self.return_All_Database_User.__name__)
        else:
            log_Info(self.return_All_Database_User.__name__)
            return self.cursor.fetchall()
