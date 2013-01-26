import unittest
# pylint: disable=W0403
from geo import GeoDB, SameCodes
import os

class Test_GeoDB(unittest.TestCase):
    def setUp(self):
        self.geo = GeoDB()

    def test_geo_get_state(self):
        testcases = [('016027', 'ID'),
                     ('047065', 'TN')]
        for code, state in testcases:
            response = self.geo.getstate(code)
            assert response == state

    def test_geo_get_scope(self):
        testcases = [(['016027', '047065'], 'US'),
                     (['016027', '016001'], 'ID'),
                     (['016027'], 'ID')]
        for codes, scope in testcases:
            response = self.geo.getfeedscope(codes)
            assert response == scope

    def test_geo_same_lookup(self):
        expected = {'state': 'ID', 'code': '016027', 'local': 'Canyon'}
        req_location = {'code': '016027'}
        response = self.geo.location_lookup(req_location)
        assert response == expected

    def test_location_lookup_false(self):
        self.geo.location_lookup('test')

    def test_samecode_lookup_false(self):
        self.geo.lookup_samecode('test', 'test')

    def test_get_states_from_samecodes_false(self):
        try:
            self.geo._get_states_from_samecodes(['999999'])
        except Exception:
            pass
        else:
            raise Exception("that should have failed")

    def test_get_states_from_samecodes_str(self):
        try:
            self.geo._get_states_from_samecodes('016027')
        except Exception:
            pass
        else:
            raise Exception("that should have failed")


    def test_forced_reload_samecodes(self):
        sc = SameCodes()
        os.remove(sc._same_cache_file)
        sc._load_same_codes()





if __name__ == '__main__':
    unittest.main()