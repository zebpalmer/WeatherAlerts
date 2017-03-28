#!/usr/bin/env python
import sys
import os
import requests
import tempfile
from six.moves import cPickle as pickle
from datetime import datetime, timedelta


class GeoDB(object):
    '''
    Interact with samecodes data
    will be adding additional data (zip code lookup) in the future.
    '''
    def __init__(self):
        self.__same = SameCodes()
        self.samecodes = self.__same.samecodes

    def location_lookup(self, req_location):
        '''
        returns full location given samecode or county and state. Returns False if not valid.

        *currently locations are a dictionary, once other geo data is added, they will move to a location class/obj*
        '''
        location = False
        try:
            location = self.samecodes[req_location['code']]
        except Exception:
            pass
        try:
            location = self.lookup_samecode(req_location['local'], req_location['state'])
        except Exception:
            pass
        return location

    def lookup_samecode(self, local, state):
        '''Given County, State return the SAME code for specified location. Return False if not found'''
        for location in self.samecodes:
            if state.lower() == self.samecodes[location]['state'].lower():
                if local.lower() == self.samecodes[location]['local'].lower():
                    return self.samecodes[location]
        return False

    def lookup_county_state(self, samecode):
        '''Given a samecode, return county, state'''
        location = self.samecodes[samecode]
        return location['local'], location['state']

    def getstate(self, geosame):
        '''Given a SAME code, return the state that SAME code is in'''
        state = self.samecodes[geosame]['state']
        return state

    def getfeedscope(self, geocodes):
        '''Given multiple SAME codes, determine if they are all in one state. If so, it returns that state.
           Otherwise return 'US'. This is used to determine which NWS feed needs to be parsed to get
           all alerts for the requested SAME codes'''
        states = self._get_states_from_samecodes(geocodes)
        if len(states) >= 2:
            return 'US'
        else:
            return states[0]

    def _get_states_from_samecodes(self, geocodes):
        '''Returns all states for a given list of SAME codes

        *Shouldn't be used to determine feed scope, please use getfeedscope()*
        '''
        states = []
        for code in geocodes:
            if not isinstance(geocodes, list):
                raise Exception("specified geocodes must be list")
            try:
                state = self.samecodes[code]['state']
            except KeyError:
                raise Exception("Samecode Not Found")
            else:
                if state not in states:
                    states.append(state)
        return states


class SameCodes(object):
    '''
    Is used to download, parse and cache the SAME codes data from the web.

    *All interaction with the SAME codes data should be done with the GeoGB object*
    '''
    def __init__(self):
        self._cachedir = str(tempfile.gettempdir()) + '/'
        self._same_cache_file = self._cachedir + 'nws_samecodes_{0}.cache'.format(sys.version_info[0])
        self._samecodes = None
        self._load_same_codes()

    @property
    def samecodes(self):
        '''public method to return the same codes list'''
        return self._samecodes

    def reload(self):
        '''force refresh of Same Codes'''
        self._load_same_codes(refresh=True)

    def _load_same_codes(self, refresh=False):
        '''Loads the Same Codes into this object'''
        if refresh is True:
            self._get_same_codes()
        else:
            self._cached_same_codes()

    def _get_same_codes(self):
        '''get SAME codes, load into a dict and cache'''
        same = {}
        url = '''http://www.nws.noaa.gov/nwr/data/SameCode.txt'''
        # pylint: disable=E1103
        raw = requests.get(url).content.decode('utf-8')  # py3 compatibility
        for row in raw.split('\n'):
            try:
                code, local, state = str(row).strip().split(',')
                location = {}
                location['code'] = code
                location['local'] = local
                #when I contacted the nws to add a missing same code
                #they added a space before the state in the samecodes file
                #stripping it out
                location['state'] = state.strip()
                same[code] = location
            finally:
                pass
        cache = open(self._same_cache_file, 'wb')
        pickle.dump(same, cache)
        cache.close()
        return same

    def _cached_same_codes(self):
        '''If a cached copy is availible, return it'''
        cache_file = self._same_cache_file
        if os.path.exists(cache_file):
            maxage = datetime.now() - timedelta(minutes=4320)
            file_ts = datetime.fromtimestamp(os.stat(cache_file).st_mtime)
            if file_ts > maxage:
                try:
                    cache = open(cache_file, 'rb')
                    self._samecodes = pickle.load(cache)
                    cache.close()
                    return True
                finally:
                    pass
        self.reload()
