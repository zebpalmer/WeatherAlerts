import unittest
# pylint: disable=W0403
from feed import AlertsFeed


class Test_Feed(unittest.TestCase):
    def setUp(self):
        self.cf = AlertsFeed(maxage=60)

    def test_refesh(self):
        self.cf.raw_cap(refresh=True)
        self.cf.raw_cap(refresh=False)




if __name__ == '__main__':
    unittest.main()