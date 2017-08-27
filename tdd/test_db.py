import unittest
import db
import mock


class TestcaseDatabase(unittest.TestCase):
    @mock.patch('db.sqlite3.connect')
    def setUp(self, mock_sqlite3_connect):
        self.mock_connection = mock_sqlite3_connect.return_value
        self.helper = db.Database()

    def test_create_table(self):
        call = "CREATE TABLE IF NOT EXISTS USERS\
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            USER_ID INTEGER INIQUE,\
            CHANNEL TEXT,\
            MESSAGE TEXT,\
            SCHEDULE TEXT)"
        self.helper
        mock_cursor = self.mock_connection.cursor()
        mock_cursor.execute.assert_called_with(call)

    def test_add_user(self):
        mock_cursor = self.mock_connection.cursor()
        user_id = 'test'
        self.helper.add_user(user_id)
        call = "INSERT OR IGNORE INTO USERS(USER_ID) VALUES(?)"
        mock_cursor.execute.assert_called_with(call, (user_id,))


if __name__ == '__main__':
    unittest.main()
