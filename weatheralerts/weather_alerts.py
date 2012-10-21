from feed import AlertsFeed
from cap import CapParser
from geo import GeoDB
from alert import Alert


class WeatherAlerts(object):
    '''
    WeatherAlerts object that controls interaction with the NWS CAP alerts feed as well and varios geo data sources.
    Most interaction from users, scripts, etc will be through the api provided by this class. So, as we approach a
    more stable project, the API in this class will also become more stable and maintain backwards compatibility.
    '''
    def __init__(self, state=None, samecodes=None, countycodes=None, load=True):
        '''
        init Alerts, default to National Feed, set state level samecodes or county codes the area in which you want to
        load alerts.
        '''
        self._alerts = None
        self.geo = GeoDB()
        self.state = state
        self.scope = 'US'
        self.samecodes = samecodes
        self.countycodes = countycodes
        if self.state is not None:
            self.scope = self.state
        elif samecodes is not None or countycodes is not None:
            self.scope = self.geo.getfeedscope(samecodes, countycodes)

        if load is True:
            self.load_alerts()

    def load_alerts(self):
        '''
        Gets raw xml (cap) from the Alerts feed, throws it into the parser
        and ends up with a list of alerts object, which it stores to self._alerts
        '''
        cap = AlertsFeed(state=self.scope).raw_cap
        parser = CapParser(cap, geo=self.geo)
        self._alerts = parser.get_alerts()

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
