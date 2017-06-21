import sqlite3
import sys

sys.path.append('../')


def save_db(user_id, text, date):
    connection = sqlite3.connect('db/test.db')

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
# ADD WRITE TO LOG FILE
    else:
        connection.commit()

    connection.close()
