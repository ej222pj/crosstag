import os
import unittest
import tempfile
import grequests
import sys
sys.path.append('./')
from config import SQLALCHEMY_DATABASE_URI
import crosstag_server


class CrosstagApiTestCase(unittest.TestCase):
    '''
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

    def test_static_tagin_page(self):
        rv = self.app.get('/crosstag/v1.0/static_tagin_page')
        assert 'Topp 5 taggningar' in rv.data.decode('utf8')

    def test_get_all_user(self):
        urls = ["http://%s:%d/crosstag/v1.0/get_user_data_tag/%s" % ("0.0.0.0", 80, "11111111")]
        unsent = (grequests.get(url) for url in urls)
        res = grequests.map(unsent)
        self.assertEqual('[<Response [500]>]', str(res))
'''

if __name__ == '__main__':
    unittest.main()
# övervakningstest
# end to end testar allt hela tiden som en slutanvändare

# Keywords som plockar bort

#MOdeldriven test MDT
#System Monitoring
#HeatMaps
