class GeoDB(object):
    '''Interact with samecodes object and other geolocation data that will be added soon'''
    def __init__(self):
        self.__same = SameCodes()
        self.samecodes = self.__same.samecodes


    def location_lookup(self, req_location):
        '''
        returns full location given samecode or county and state. Returns False if not valid.
        *currently locations are a dictionary, once other geo data is added, they will move to a location class/obj*
        '''
        location = False
        locations = self.samecodes
        try:
            location = locations[req_location['code']]
        except KeyError:
            pass
        try:
            location = self.lookup_samecode(req_location['local'], req_location['state'])
        except KeyError:
            pass
        return location


    def lookup_samecode(self, local, state):
        '''Given County, State return the SAME code for specified location. Return False if not found'''
        for location in self.samecodes:
            if state == self.samecodes[location]['state']:
                if local == self.samecodes[location]['local']:
                    return self.samecodes[location]
        return False

    def getstate(self, geosame):
        '''Given a SAME code, return the state that SAME code is in'''
        state = self.samecodes[geosame]['state']
        return state


    def getfeedscope(self, geocodes):
        '''Given multiple SAME codes, determine if they are all in one state. If so, it returns that state.
           Otherwise return 'US'. This is used to determine which NWS feed needs to be parsed to get
           all alerts for the requested SAME codes'''
        states = self.get_states_from_samecodes(geocodes)
        if len(states) >= 2:
            return 'US'
        else:
            return states[0]


    def get_states_from_samecodes(self, geocodes):
        '''Returns all states for a given list of SAME codes
        *Shouldn't be used to determine feed scope, please use getfeedscope()*

        '''
        states = []
        for code in geocodes:
            try:
                state = self.samecodes[code]['state']
            except KeyError:
                if not isinstance(geocodes, list):
                    print ("specified geocodes must be list")
                    raise
                else:
                    print("SAMECODE Not found")
            if state not in states:
                states.append(state)
        return states



#### GET/PARSE SAME CODES TABLE ##############################################################

class SameCodes(object):
    '''
    Is used to download, parse and cache the SAME codes data from the web.
    *All interaction with the SAME codes data should be done in the GeoGB classy*
    '''
    def __init__(self):
        self._cachedir = str(tempfile.gettempdir()) + '/'
        self._same_cache_file = self._cachedir + 'nws_samecodes.cache'
        self._load_same_codes()

    @property
    def samecodes(self):
        '''public method to return the same codes list'''
        return self._samecodes


    def reload(self):
        '''force refresh of Same Codes (mainly for testing)'''
        self._load_same_codes(refresh=True)


    def _load_same_codes(self, refresh=False):
        '''Loads the Same Codes into this object'''
        if refresh == True:
            self._get_same_codes()
        else:
            cached = self._cached_same_codes()
            if cached == None:
                self._samecodes = self._get_same_codes()


    def _get_same_codes(self):
        '''get SAME codes, load into a dict and cache'''
        same = {}
        url = '''http://www.nws.noaa.gov/nwr/SameCode.txt'''
        codes_file = request.urlopen(url)
        for row in codes_file.readlines():
            try:
                code, local, state = str(row, "utf-8").strip().split(',')
                location = {}
                location['code'] = code
                location['local'] = local
                #when I contacted the nws to add a missing same code
                #they added a space before the state in the samecodes file
                #stripping it out
                location['state'] = state.strip()
                same[code] = location
            except ValueError:
                pass
        cache = open(self._same_cache_file, 'wb')
        pickle.dump(same, cache)
        cache.close()
        return same


    def _cached_same_codes(self):
        '''If a cached copy is availible, return it'''
        cache_file = self._same_cache_file
        if os.path.exists(cache_file):
            now = datetime.now()
            maxage = now - timedelta(minutes=4320)
            file_ts = datetime.fromtimestamp(os.stat(cache_file).st_mtime)
            if file_ts > maxage:
                try:
                    cache = open(cache_file, 'rb')
                    self._samecodes = pickle.load(cache)
                    cache.close()
                    #print "Loaded SAME codes from Cache"
                    return True
                except Exception:
                    # if any problems opening cache, ignore and move on
                    return None
            else:
                #print "SAME codes cache is old, refreshing from web"
                return None
        else:
            #print "No SAME codes cache availible, loading from web"
            return None