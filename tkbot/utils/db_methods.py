import sqlite3
import sys


sys.path.append('../')


import settings


# TAKE DB_PATH FROM SETTINGS.PY...
db_path = 'db/test.db'


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

filehandler = logging.FileHandler(settings.logs_path)
filehandler.setFormatter(formatter)
filehandler.setLevel(logging.ERROR)

copy_filehandler = logging.FileHandler(settings.copy_logs_path)
copy_filehandler.setFormatter(formatter)
copy_filehandler.setLevel(logging.ERROR)

logger.addHandler(console)
logger.addHandler(filehandler)
logger.addHandler(copy_filehandler)

#########################################################################
#  FUNCTIONS ############################################################
#########################################################################


def logErr(err, function_name):
    logger.exception('Error: %s. Fucntion: %s', err,
                     function_name)


def logInfo(function_name):
    logger.info('%s - success', function_name)

##########################################################################


def appendMessageDatabase(user_id, text, date):
    connection = sqlite3.connect(db_path)

    cursor = connection.cursor()

    sql = """ CREATE TABLE IF NOT EXISTS ADV_USERS
    (PID INTEGER PRIMARY KEY AUTOINCREMENT,
    USR_ID INT,
    MESSAGE TEXT,
    DATE INT) """

    cursor.execute(sql)

    sql = "INSERT INTO ADV_USERS(USR_ID, MESSAGE, DATE) VALUES(?, ?, ?)"
    params = (user_id, text, date)

    try:
        cursor.execute(sql, params)
        connection.commit()
    except sqlite3.DatabaseError as err:
        print('Error:', err)
        logErr(err, appendMessageDatabase.__name__)
    else:
        connection.commit()
        logInfo(appendMessageDatabase.__name__)

    connection.close()


def popMessageDatabase():
    pass


def findDuplicateMessageDatabase():
    pass
