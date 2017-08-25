import unittest
import db
import mock


class TestcaseDatabase(unittest.TestCase):
    @mock.patch('db.sqlite3.connect')
    def setUp(self, mock_sqlite3_connect):
        self.mock_connection = mock_sqlite3_connect.return_value
        db.Database()

    def test_create_table(self):
        call = "CREATE TABLE IF NOT EXISTS USER\
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            USER_ID INTEGER INIQUE,\
            CHANNEL TEXT,\
            MESSAGE TEXT,\
            SCHEDULE TEXT)"
        mock_cursor = self.mock_connection.cursor()
        mock_cursor.execute.assert_called_with(call)


if __name__ == '__main__':
    unittest.main()
