import unittest
import grequests
#from crosstag_server import get_all_users


class TestStringMethods(unittest.TestCase):

    def test_get_all_user(self):
        urls = ["http://%s:%d/crosstag/v1.0/get_user_data_tag/%s" % ("0.0.0.0", 80, "11111111")]
        unsent = (grequests.get(url) for url in urls)
        res = grequests.map(unsent)
        print("Res is =  " + res)
        self.assertIsNone(res)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
