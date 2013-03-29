# pylint: disable=W0403
from feed import AlertsFeed
from cap import CapParser
from geo import GeoDB


class WeatherAlerts(object):
    '''
    WeatherAlerts object that controls interaction with the NWS CAP alerts feed as well as varios geo data sources.
    Most interaction from users, scripts, etc will be through the api provided by this `WeatherAlerts` class.
    So, as we approach a more stable project, the API in this class will also become more stable.

    * Defaults to National Feed, it can be quite large at times, you probably don't want to parse it very often.
    * Set `state` to see all alerts on your state feed.
    * For local alerts only, set `samecodes` to a single samecode string, or list of samecode strings.
    * `cachetime` is set in minutes, default is 3.

    '''
    def __init__(self, state=None, samecodes=None, load=True, cachetime=3):
        '''
        WeatherAlerts Init
        '''
        self._alerts = None
        self._feed = None
        self.geo = GeoDB()
        self.state = state
        self.scope = 'US'
        self.cachetime = cachetime
        if samecodes is None:
            self.samecodes = None
        elif isinstance(samecodes, str):
            self.samecodes = []
            self.samecodes.append(samecodes)
        elif isinstance(samecodes, list):
            self.samecodes = samecodes
        else:
            raise Exception("Samecode must be string, or list of strings")
        if self.state is not None:
            self.scope = self.state
        elif samecodes is not None:
            self.scope = self.geo.getfeedscope(self.samecodes)

        if load is True:
            self.load_alerts()

    def load_alerts(self):
        '''
        NOTE: use refresh() instead of this, if you are just needing to refresh the alerts list
        Gets raw xml (cap) from the Alerts feed, throws it into the parser
        and ends up with a list of alerts object, which it stores to self._alerts
        '''
        self._feed = AlertsFeed(state=self.scope, maxage=self.cachetime)
        parser = CapParser(self._feed.raw_cap(), geo=self.geo)
        self._alerts = parser.get_alerts()

    def refresh(self, force=False):
        '''
        Refresh the alerts list. set `force` to True to force pulling a new list from the NWS, otherwise
        it'll only pull a new list if the cached copy is expired. (see cachetime)
        '''
        if force is True:
            self._feed.refresh()
        self._alerts = CapParser(self._feed.raw_cap(), geo=self.geo).get_alerts()

    @property
    def alerts(self):
        '''returns the alerts list. If samecode(s) are specified when the WeatherAlerts object is created,
        this will only return alerts for those samecodes. If no samecodes were given, it'll return all alerts for the
        state if one was specified otherwise for the entire U.S.
        '''
        if self.samecodes is not None:
            temp = []
            for alert in self._alerts:
                for code in alert.samecodes:
                    if code in self.samecodes:
                        temp.append(alert)
            return temp
        else:
            return self._alerts

    @property
    def _serialized_alerts(self):
        '''returns a list of alerts, jsonified'''
        return [x._serialized for x in self.alerts]


    def samecode_alerts(self, samecode):
        '''Returns alerts for a ()single) SAME geocode. Only useful if you didn't specify samecodes when the WeatherAlerts
        object was created.'''
        return [x for x in self._alerts if samecode in x.samecodes]

    def county_state_alerts(self, county, state):
        '''Given a county and state, return alerts'''
        samecode = self.geo.lookup_samecode(county, state)
        return self.samecode_alerts(samecode)

    def event_state_counties(self):
        '''DEPRECATED: this will be moved elsewhere or dropped in the near future, stop using it.
        Return an event type and it's state(s) and counties (consolidated)'''
        # FIXME: most of this logic should be moved to the alert instance and refactored
        for alert in self._alerts:
            locations = []
            states = []
            for samecode in alert.samecodes:
                county, state = self.geo.lookup_county_state(samecode)
                locations.append((county, state))
                if state not in states:
                    states.append(state)
            for state in states:
                counties = [x for x, y in locations if y == state]
            counties_clean = str(counties).strip("[']")
            print "{0}: {1} - {2}".format(alert.event, state, counties_clean)
