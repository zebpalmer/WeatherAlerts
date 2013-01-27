import unittest
# pylint: disable=W0403,W0212,W0612
from weather_alerts import WeatherAlerts


class Test_WeatherAlerts(unittest.TestCase):
    def setUp(self):
        self.nws = WeatherAlerts()

    def test_almost_everything(self):
        print "Alerts currently in feed {0}".format(self.nws.alert_count)

    def test_event_state_counties(self):
        self.nws.event_state_counties()

    def test_samecode_alerts_method(self):
        self.nws.samecode_alerts('016027')

    def test_county_state_alerts(self):
        self.nws.county_state_alerts('canyon', 'ID')

    def test_alert_attributes(self):
        for alert in self.nws.alerts:
            x = alert.title
            x = alert.summary
            x = alert.areadesc
            x = alert.event
            x = alert.samecodes
            x = alert.zonecodes
            x = alert.expiration
            x = alert.updated
            x = alert.effective
            x = alert.published
            x = alert.severity
            x = alert.category
            x = alert.urgency


    def test_passing_samecodes(self):
        # Alerts by a Samecode
        nws = WeatherAlerts(samecodes='016027')
        nws = WeatherAlerts(samecodes=['016027','016001','016073','016075'])
        for alert in nws.alerts:
            x = alert.title
            x = alert.summary
            x = alert.areadesc
            x = alert.event
            x = alert.samecodes
            x = alert.zonecodes
            x = alert.expiration
            x = alert.updated
            x = alert.effective
            x = alert.published
            x = alert.severity
            x = alert.category
            x = alert.urgency


    def test_passing_state(self):
        nws = WeatherAlerts(state='ID')
        for alert in nws.alerts:
            x = alert.title
            x = alert.summary
            x = alert.areadesc
            x = alert.event
            x = alert.samecodes
            x = alert.zonecodes
            x = alert.expiration
            x = alert.updated
            x = alert.effective
            x = alert.published
            x = alert.severity
            x = alert.category
            x = alert.urgency

    def test_break_on_samecodes(self):
        '''break if you pass in non str/list samecodes'''
        try:
            nws = WeatherAlerts(samecodes=1)
        except Exception:
            pass
        else:
            raise Exception("That shouldn't have worked")





if __name__ == '__main__':
    unittest.main()