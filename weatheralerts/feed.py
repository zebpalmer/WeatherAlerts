class CapAlertsFeed(object):
    '''Fetch and load the NWS CAP/XML Alerts feed for the US or a single state if requested
       if an instance of the SameCodes class has already been (to do a geo lookup), you can pass that
       as well to save some processing'''
    def __init__(self, state='US', geo=None, maxage=3, reload=False):
        self._alerts = ''
        self._feedstatus = ''
        self._cachetime = maxage
        self.state = self._set_state(state, refresh=False)
        self._cachedir = str(tempfile.gettempdir()) + '/'
        self._alert_cache_file = self._cachedir + 'nws_alerts_%s.cache' % (self.state)
        if geo == None:
            self.geo = GeoDB()
        else:
            self.geo = geo
        self.samecodes = self.geo.samecodes

        self._cachetime = 3
        self._alerts_ts = datetime.now()
        self._lookuptable = {}
        self._reload = reload
        # now for the real work
        self._load_alerts()
        


    @property
    def alerts(self):
        '''returns all alerts on feed'''
        self.check_objectage()
        return self._alerts


    def _set_state(self, state, refresh=True):
        '''sets state, reloads alerts unless told otherwise'''
        if len(state) == 2:
            self.state = state.upper()
            if refresh == True:
                self._alert_cache_file = self._cachedir + 'self.alerts_%s.cache' % (self.state)
                self._load_alerts()
            return state
        else:
            raise Exception('Error parsing given state')


    def reload_alerts(self):
        '''Reload alerts bypassing cache'''
        self._load_alerts(refresh=True)


    def check_objectage(self):
        '''check age of alerts in this object, reload if past max cache time'''
        now = datetime.now()
        maxage = now - timedelta(minutes=self._cachetime)
        if self._alerts_ts > maxage:
            self.reload_alerts()


    def _cached_alertobj(self):
        '''If a recent cache exists, return it'''
        if os.path.exists(self._alert_cache_file):
            now = datetime.now()
            maxage = now - timedelta(minutes=self._cachetime)
            file_ts = datetime.fromtimestamp(os.stat(self._alert_cache_file).st_mtime)
            if file_ts > maxage:
                try:
                    cache = open(self._alert_cache_file, 'rb')
                    alerts = pickle.load(cache)
                    cache.close()
                except Exception:
                    # if any problems loading cache file, ignore and move on
                    # (this is here to prevent issues switching between python2 and python3)
                    alerts = None
            else:
                #"Alerts cache is old"
                alerts = None
        else:
            #"No Alerts cache availible"
            alerts = None
        return alerts


    def _load_alerts(self, refresh=False):
        '''Load the alerts feed and parse it'''
        if refresh == True:
            self._alerts = self._parse_cap(self._get_nws_feed())
        elif refresh == False:
            cached = self._cached_alertobj()
            if cached == None:
                self._alerts = self._parse_cap(self._get_nws_feed())
            else:
                self._alerts = cached


    def _get_nws_feed(self):
        '''get nws alert feed, and cache it'''
        url = '''http://alerts.weather.gov/cap/%s.php?x=0''' % (self.state)
        feed = request.urlopen(url)
        xml = feed.readall()
        return xml

    def _parse_cap(self, xmlstr):
        '''parse and cache the feed contents'''
        main_dom = minidom.parseString(xmlstr)

        xml_entries = main_dom.getElementsByTagName('entry')
        tags = ['title', 'updated', 'published', 'id', 'summary', 'cap:effective', 'cap:expires', 'cap:status',
                'cap:msgType', 'cap:category', 'cap:urgency', 'cap:severity', 'cap:certainty', 'cap:areaDesc',
                'cap:geocode']

        entry_num = 0
        alerts = {}
        pat = re.compile('(.*) issued')
        for dom in xml_entries:
            entry_num = entry_num + 1
            entry = {}
            for tag in tags:
                try:
                    if tag == 'cap:geocode':
                        try:
                            entry['geocodes'] = str(dom.getElementsByTagName('value')[0].firstChild.data).split(' ')
                        except AttributeError:
                            entry['geocodes'] = []
                    else:
                        try:
                            entry[tag] = dom.getElementsByTagName(tag)[0].firstChild.data
                            if entry['title'] == "There are no active watches, warnings or advisories":
                                return {}
                        except AttributeError:
                            pass
                except IndexError:
                    return {}
            entry['type'] = pat.match(entry['title']).group(1)
            
            locations = []
            for geo in entry['geocodes']:
                try:
                    location = self.samecodes[geo]
                except KeyError:
                    location = { 'code': geo,
                                 'local': geo,
                                 'state': 'unknown'}
                locations.append(location)

                # We're going to create a table to reference alerts by
                # TODO: make all alert lookups use the resulting data 
                self._create_lookuptable(geo, entry_num, entry['type'])

            target_areas = []
            areas = str(entry['cap:areaDesc']).split(';')
            for area in areas:
                target_areas.append(area.strip())
            entry['locations'] = locations
            entry['target_areas'] = target_areas
            alerts[entry_num] = entry
            del entry
        # cache alerts data
        cache = open(self._alert_cache_file, 'wb')
        pickle.dump(alerts, cache)
        cache.close()
        self._alerts_ts = datetime.now()
        return alerts

    def _create_lookuptable(self, samecode, alert_num, alert_type):
        alert_tuple = (alert_num, alert_type)
        if samecode in self._lookuptable:
            self._lookuptable[samecode].append(alert_tuple)
        else:
            _alertids = []
            _alertids.append(alert_tuple)
            self._lookuptable[samecode] = _alertids
    