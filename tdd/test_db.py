import unittest
import db
import mock


class TestcaseDatabase(unittest.TestCase):
    @mock.patch('db.sqlite3.connect')
    def setUp(self, mock_sqlite3_connect):
        self.mock_connection = mock_sqlite3_connect.return_value
        self.fixture = db.Database()

    def test_create_table(self):
        mock_cursor = self.mock_connection.cursor()

        call = "CREATE TABLE IF NOT EXISTS USERS\
            (ID INTEGER PRIMARY KEY AUTOINCREMENT,\
            USER_ID INTEGER INIQUE,\
            CHANNEL TEXT,\
            MESSAGE TEXT,\
            SCHEDULE TEXT)"

        self.fixture
        mock_cursor.execute.assert_called_with(call)

    def test_add_user(self):
        mock_cursor = self.mock_connection.cursor()

        user_id = 'user_id'
        call = "INSERT OR IGNORE INTO USERS(USER_ID) VALUES(?)"

        self.fixture.add_user(user_id)
        mock_cursor.execute.assert_called_with(call, (user_id,))

    def test_update_channel(self):
        mock_cursor = self.mock_connection.cursor()

        channel, user_id = 'channel', 'user_id'
        call = "UPDATE USERS SET CHANNEL=? WHERE USER_ID=?"

        self.fixture.update_channel(channel, user_id)
        mock_cursor.execute.assert_called_with(call, (channel, user_id,))

    def test_update_message(self):
        mock_cursor = self.mock_connection.cursor()

        message, user_id = 'message', 'user_id'
        call = "UPDATE USERS SET MESSAGE=? WHERE USER_ID=?"

        self.fixture.update_message(message, user_id)
        mock_cursor.execute.assert_called_with(call, (message, user_id,))

    def test_update_schedule(self):
        mock_cursor = self.mock_connection.cursor()

        schedule, user_id = 'schedule', 'user_id'
        call = "UPDATE USERS SET SCHEDULE=? WHERE USER_ID=?"

        self.fixture.update_schedule(schedule, user_id)
        mock_cursor.execute.assert_called_with(call, (schedule, user_id,))


if __name__ == '__main__':
    unittest.main()
