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

    def update_channel(self, channel, user_id):
        self.add_user(user_id)

        sql = "UPDATE USERS SET CHANNEL=? WHERE USER_ID=?"

        cursor = self.connection.cursor()
        cursor.execute(sql, (channel, user_id,))

        self.connection.commit()

    def update_message(self, message, user_id):
        self.add_user(user_id)

        sql = "UPDATE USERS SET MESSAGE=? WHERE USER_ID=?"

        cursor = self.connection.cursor()
        cursor.execute(sql, (message, user_id,))

        self.connection.commit()

    def update_schedule(self, schedule, user_id):
        self.add_user(user_id)

        sql = "UPDATE USERS SET SCHEDULE=? WHERE USER_ID=?"

        cursor = self.connection.cursor()
        cursor.execute(sql, (schedule, user_id,))

        self.connection.commit()
