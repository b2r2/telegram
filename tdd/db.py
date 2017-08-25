import sqlite3
import settings


class Database():
    def __init__(self):
        self.connection = sqlite3.connect(settings.db,
                                          check_same_thread=False)
        self.connection.cursor()
        sql = "CREATE TABLE IF NOT EXISTS USER\
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            USER_ID INTEGER INIQUE,\
            CHANNEL TEXT,\
            MESSAGE TEXT,\
            SCHEDULE TEXT)"
        self.connection.execute(sql)
        self.connection.commit()
