import os
import unittest
import tempfile
import sys
sys.path.append('./')
from config import SQLALCHEMY_DATABASE_URI
import crosstag_server


class CrosstagTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, crosstag_server.app.config[SQLALCHEMY_DATABASE_URI] = tempfile.mkstemp()
        crosstag_server.app.config['TESTING'] = True
        self.app = crosstag_server.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(crosstag_server.app.config[SQLALCHEMY_DATABASE_URI])

    def test_front_page(self):
        rv = self.app.get('/')
        assert 'Cloudtag' in rv.data.decode('utf8')


if __name__ == '__main__':
    unittest.main()