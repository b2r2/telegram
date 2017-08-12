import unittest
import db
import mock


class TestcaseDatabase(unittest.TestCase):
    @mock.patch('db.sqlite3.connect')
    def test_database_create_table_call(self, mock_sqlite3_connect):
        sqlite_execute_mock = mock.Mock()
        mock_sqlite3_connect.return_value = sqlite_execute_mock
        db.Database()
        call = "CREATE TABLE IF NOT EXISTS USER\
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            USER_ID INTEGER INIQUE,\
            CHANNEL_NAME TEXT,\
            MESSAGE TEXT,\
            SCHEDULE TEXT)"
        sqlite_execute_mock.execute.assert_called_with(call)


if __name__ == '__main__':
    unittest.main()
