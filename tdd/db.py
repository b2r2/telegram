import sqlite3
import settings


class Database():
    def __init__(self):
        self.connection = sqlite3.connect(settings.db,
                                          check_same_thread=False)
        self.create_table()

    def create_table(self):
        sql = "CREATE TABLE IF NOT EXISTS USERS\
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            USER_ID INTEGER INIQUE,\
            CHANNEL TEXT,\
            MESSAGE TEXT,\
            SCHEDULE TEXT)"
        cursor = self.connection.cursor()
        cursor.execute(sql)
        self.connection.commit()

    def add_user(self, user_id):
        sql = "INSERT OR IGNORE INTO USERS(USER_ID) VALUES(?)"
        cursor = self.connection.cursor()
        cursor.execute(sql, (user_id,))
        self.connection.commit()
