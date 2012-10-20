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

        if load == True:
            self.load_alerts()

    def load_alerts(self):
        '''
        Gets raw xml (cap) from the Alerts feed, throws it into the parser
        and ends up with a list of alerts object, which it stores to self._alerts
        '''
        cap = AlertsFeed(state=self.state).raw_cap
        self._alerts = CapParser(cap, geo=self.geo)

    @property
    def alert_count(self):
        '''simple property for checking the number of alerts, mainly for debugging purposes'''
        return len(self._alerts)




if __name__ == '__main__':
    nws = WeatherAlerts(state='ID')
    print nws.alert_count