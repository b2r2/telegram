import sqlite3
import sys


sys.path.append('../')


import settings
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

filehandler = logging.FileHandler(settings.logs)
filehandler.setFormatter(formatter)
filehandler.setLevel(logging.ERROR)

copy_filehandler = logging.FileHandler(settings.copy_logs)
copy_filehandler.setFormatter(formatter)
copy_filehandler.setLevel(logging.ERROR)

logger.addHandler(console)
logger.addHandler(filehandler)
logger.addHandler(copy_filehandler)

#########################################################################
#  FUNCTIONS ############################################################
#########################################################################


def logErr(function_name, msg):
    logger.exception('Error:  %s. Sending a file(type %s)',
                     function_name, msg)


def logInfo(function_name):
    logger.info('%s: success', function_name)

##########################################################################

db_path = 'db/test.db'


class Database():
    def __init__(self):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
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
            logErr(err, self.__init__.__name__)
        else:
            logInfo(self.__init__.__name__)

# DEBUG#######################################

    def viewTable(self):
        sql = "SELECT * FROM ADV_USERS"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

###############################################
# INSERT OR UPDATE METHODS ####################
###############################################
    def insertDb(self, user_id):
        """ Insert database """
        sql = "INSERT OR IGNORE INTO ADV_USERS(USER_ID) VALUES(?)"
        try:
            self.cursor.execute(sql, (user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.insertDb.__name__)

    def handleAdvMessageUser(self, user_id, message, date):
        """ Insert or Update advertising message """
        self.insertDb(user_id)
        sql = "UPDATE ADV_USERS SET MESSAGE=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (message, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.handleAdvMessageUser.__name__)
        else:
            logInfo(self.handleAdvMessageUser.__name__)

    def handleChannelUser(self, user_id, channel, date):
        """ Insert or Update channel name """
        self.insertDb(user_id)
        sql = "UPDATE ADV_USERS SET CHANNEL=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (channel, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.handleChannelUser.__name__)
        else:
            logInfo(self.handleChannelUser.__name__)

    def handleScheduleUser(self, user_id, sched, date):
        """ Insert or Update schedule """
        self.insertDb(user_id)
        sql = "UPDATE ADV_USERS SET SCHEDULE=?, DATE=? WHERE USER_ID=?"
        try:
            self.cursor.execute(sql, (sched, date, user_id,))
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.handleScheduleUser.__name__)
        else:
            logInfo(self.handleScheduleUser.__name__)

###############################################
# RETURN METHODS ##############################
###############################################

    def returnAdvMessageUser(self, user_id):
        """ Return advertising message """
        sql = "SELECT MESSAGE FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.returnAdvMessageUser.__name__)
        else:
            logInfo(self.returnAdvMessageUser.__name__)
            return self.cursor.fetchall()

    def returnChannelUser(self, user_id):
        """ Return Channel name """
        sql = "SELECT CHANNEL FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.returnChannelUser.__name__)
        else:
            logInfo(self.returnChannelUser.__name__)
            return self.cursor.fetchall()

    def returnScheduleUser(self, user_id):
        """ Return schedule """
        sql = "SELECT SCHEDULE FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.returnScheduleUser.__name__)
        else:
            logInfo(self.returnScheduleUser.__name__)
            return self.cursor.fetchall()

    def returnAllDataUser(self, user_id):
        """ Return all the data about the user """
        sql = "SELECT * FROM ADV_USERS WHERE USER_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.returnAllDataUser.__name__)
        else:
            logInfo(self.returnAllDataUser.__name__)
            return self.cursor.fetchall()
