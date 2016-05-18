import os
import unittest
import tempfile
import grequests
import sys
from datetime import datetime
sys.path.append('./')
from db_service import users_sql_client as user_client

class CrosstagApiTestCase(unittest.TestCase):

    def test_send_tagevent_pass(self):
        try:
            now = datetime.now()
            urls = ["http://%s:%d/crosstag/v1.0/tagevent/%s/%s/%s" % ("0.0.0.0.", 80, "11111111",
                                                                      '2F80D9B8-AAB1-40A1-BC26-5DA4DB3E9D9B', str(now))]
            unsent = (grequests.get(url) for url in urls)
            res = grequests.map(unsent)
            self.assertEqual('[<Response [200]>]', str(res))
        except KeyError as error:
            self.fail(error.value)

    def test_send_tagevent_fail(self):
        try:
            now = datetime.now()
            urls = ["http://%s:%d/crosstag/v1.0/tagevent/%s/%s/%s" % ("0.0.0.0.", 80, "11111111",
                                                                      '2F80D9B8-AAB1-40A1-BC26-5DA4DB3E', str(now))]
            unsent = (grequests.get(url) for url in urls)
            res = grequests.map(unsent)
            self.assertEqual('[<Response [500]>]', str(res))
        except KeyError as error:
            self.fail(error.value)

    def test_get_user_pass(self):
        self.fail('tja')

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
