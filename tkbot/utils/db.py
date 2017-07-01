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
# DEBUG#######################################

    def viewTable(self):
        sql = "SELECT * FROM ADV_USERS"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
###############################################

    def updateAdvMessageUser(self, user_id, message, date):
        """ Update advertising message """
        returnSelectUserId = self.returnSelectUserId()
        if returnSelectUserId and user_id in returnSelectUserId:
            sql = "UPDATE ADV_USERS SET MESSAGE=(?), DATE=(?)"
            try:
                self.cursor.execute(sql, (message, date,))
                self.connection.commit()
            except sqlite3.DatabaseError as err:
                logErr(err, self.updateAdvMessageUser.__name__)
            else:
                logInfo(self.updateAdvMessageUser.__name__)
        else:
            self.addAdvMessageUser(user_id, message, date)

    def addAdvMessageUser(self, user_id, message, date):
        """ Insert or replace advertising message """
        sql = "INSERT OR REPLACE INTO ADV_USERS(USER_ID, MESSAGE, DATE) VALUES(?, ?, ?)"
        params = (user_id, message, date)

        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.addAdvMessageUser.__name__)
        else:
            logInfo(self.addAdvMessageUser.__name__)

    def updateChannelUser(self, user_id, channel, date):
        """ Update channel name """
        returnSelectUserId = self.returnSelectUserId()
        if returnSelectUserId and user_id in returnSelectUserId:
            sql = "UPDATE ADV_USERS SET CHANNEL=(?), DATE=(?)"
            try:
                self.cursor.execute(sql, (channel, date,))
                self.connection.commit()
            except sqlite3.DatabaseError as err:
                logErr(err, self.updateChannelUser.__name__)
            else:
                logInfo(self.updateChannelUser.__name__)
        else:
            self.addChannelUser(user_id, channel, date)

    def addChannelUser(self, user_id, channel, date):
        """ Insert or replace channel name """
        sql = "INSERT OR REPLACE INTO ADV_USERS(USER_ID, CHANNEL, DATE) VALUES(?, ?, ?)"
        params = (user_id, channel, date,)
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.addChannelUser.__name__)
        else:
            logInfo(self.addChannelUser.__name__)

    def updateScheduleUser(self, user_id, sched, date):
        """ Update schedule """
        returnSelectUserId = self.returnSelectUserId()
        if returnSelectUserId and user_id in returnSelectUserId:
            sql = "UPDATE ADV_USERS SET SCHEDULE=(?), DATE=(?)"
            try:
                self.cursor.execute(sql, (sched, date,))
                self.connection.commit()
            except sqlite3.DatabaseError as err:
                logErr(err, self.updateScheduleUser.__name__)
            else:
                logInfo(self.updateScheduleUser.__name__)
        else:
            self.addScheduleUser(user_id, sched, date)

    def addScheduleUser(self, user_id, sched, date):
        """ Insert or replace schedule """
        sql = "INSERT OR REPLACE INTO ADV_USERS(USER_ID, SCHEDULE, DATE) VALUES(?, ?, ?)"
        params = (user_id, sched, date)
        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.addScheduleUser.__name__)
        else:
            logInfo(self.addScheduleUser.__name__)

    def returnSelectUserId(self):
        sql = "SELECT USER_ID FROM ADV_USERS"
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.returnSelectUserId.__name__)
        else:
            logInfo(self.returnSelectUserId.__name__)
            return self.cursor.fetchone()
