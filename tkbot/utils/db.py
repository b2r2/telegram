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
              USR_ID INTEGER UNIQUE,
              MESSAGE TEXT,
              DATE INTEGER) """
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.__init__.__name__)
        else:
            logInfo(self.__init__.__name__)

    def takeUserID(self, user_id):
        sql = "SELECT USR_ID FROM ADV_USERS WHERE USR_ID LIKE {}".format(user_id)
        try:
            self.cursor.execute(sql)
        except sqlite3.DatabaseError as err:
            logErr(err, self.takeUserID.__name__)
        else:
            logInfo(self.takeUserID.__name__)
            user_id = self.cursor.fetchone()
            print("This users write: {}".format(user_id))

    def replaceMessage(self, user_id, message, date):
        sql = " REPLACE INTO ADV_USERS(USR_ID, MESSAGE, DATE) VALUES(?, ?, ?) "
        params = (user_id, message, date)

        try:
            self.cursor.execute(sql, params)
            self.connection.commit()
        except sqlite3.DatabaseError as err:
            logErr(err, self.replaceMessage.__name__)
        else:
            logInfo(self.replaceMessage.__name__)
