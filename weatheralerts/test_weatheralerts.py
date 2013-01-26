import unittest
from weatheralerts import WeatherAlerts


class Test_WeatherAlerts(unittest.TestCase):
    def setUp(self):
        self.nws = WeatherAlerts()

    def test_almost_everything(self):
        print "Alerts currently in feed {0}".format(self.nws.alert_count)

    def test_geo_get_state(self):
        testcases = [('016027', 'ID'),
                     ('047065', 'TN')]
        for code, state in testcases:
            response = self.nws.geo.getstate(code)
            assert response == state

    def test_geo_get_scope(self):
        testcases = [(['016027', '047065'], 'US'),
                     (['016027', '016001'], 'ID'),
                     (['016027'], 'ID')]
        for codes, scope in testcases:
            response = self.nws.geo.getfeedscope(codes)
            assert response == scope

    def test_same_lookup(self):
        expected = {'state': 'ID', 'code': '016027', 'local': 'Canyon'}
        req_location = {'code': '016027'}
        response = self.nws.geo.location_lookup(req_location)
        assert response == expected

if __name__ == '__main__':
    unittest.main()
