import sqlite3
import settings


class Database():
    def __init__(self):
        self.connection = sqlite3.connect(settings.db,
                                          check_same_thread=False)
        self.create_table()

    def create_table(self):
        sql = "CREATE TABLE IF NOT EXISTS USER\
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            USER_ID INTEGER INIQUE,\
            CHANNEL TEXT,\
            MESSAGE TEXT,\
            SCHEDULE TEXT)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()
