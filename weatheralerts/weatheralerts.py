from feed import AlertsFeed
from cap import CapParser
from geo import GeoDB
from alert import Alert


class WeatherAlerts(object):
    '''
    WeatherAlerts object that controls interaction with the samecodes and capparser classes/methods.
    Pass state='' or geocodes='samecodes_list' to change which feed is being parsed
    passing a list of samecodes will determine if they are in the same state and pick
    the correct feed or use the US feed if they're in different states

    You can find your location's samecode by looking checking the following link
    http://www.nws.noaa.gov/nwr/indexnw.htm#sametable
    '''
    def __init__(self, state=None, geocodes=None, load=True):
        '''
        init Alerts, default to National Feed, set state or geocodes to define a feed for a given area.
        if geocodes are specified, then all alerts objects will be limited to those areas
        '''
        self._alerts = None
        self.state = state
        self.geo = GeoDB()
        if geocodes is None:
            if self.state is None:
                self.scope = 'US'
            else:
                self.scope = state
        else:
            self.scope = self.geo.getfeedscope(geocodes)

        if load is True:
            self.load_alerts()

    def load_alerts(self):
        '''
        Gets raw xml (cap) from the Alerts feed, throws it into the parser
        and ends up with a list of alerts object, which it stores to self._alerts
        '''
        cap = AlertsFeed(state=self.scope).raw_cap
        parser = CapParser(geo=self.geo)
        self._alerts = parser.cap(cap)

    @property
    def alert_count(self):
        '''simple property for checking the number of alerts, mainly for debugging purposes'''
        return len(self._alerts)

    def samecode_alerts(self, samecode):
        '''Returns alerts for specified SAME geocodes'''
        return [x for x in self._alerts if samecode in x.samecodes]

    def county_state_alerts(self, county, state):
        '''Given a county and state, return alerts'''
        samecode = self.geo.lookup_samecode(county, state)
        return self.samecode_alerts(samecode)

    def event_state_counties(self):
        '''Return an event type and it's state(s) and counties (consolidated)'''
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

if __name__ == '__main__':
    nws = WeatherAlerts()
    nws.event_state_counties()
