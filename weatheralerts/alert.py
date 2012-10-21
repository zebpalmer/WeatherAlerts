from dateutil.parser import parse
from datetime import datetime


class Alert():
    '''
    Create an alert object with the cap dict created from cap xml parser.

    This object won't be pretty... it's mostly a bunch of property methods to
    sanitize and muck around with the raw cap data. Using individual properties
    and methods instead of a special getattr so that we can more easily standardize
    the Alert API. This may be revisted in the future as the project becomes more
    stable.


    '''
    def __init__(self, cap_dict):
        self._raw = cap_dict

    def _ts_parse(self, ts):
        dt = parse(ts)
        return dt

    @property
    def summary(self):
        '''Alert summary'''
        return self._raw['summary']

    @property
    def areadesc(self):
        '''A more generic area description'''
        return self._raw['cap:areaDesc']

    @property
    def event(self):
        '''alert event type'''
        return self._raw['cap:event']

    @property
    def samecodes(self):
        '''samecodes for the alert area'''
        return self._raw['samecodes']

    @property
    def countycodes(self):
        '''UCG county codes for the alert area'''
        return self._raw['countycodes']

    @property
    def expiration(self):
        '''Expiration of the alert (datetime object)'''
        ts = self._ts_parse(self._raw['cap:expires'])
        return ts

    @property
    def updated(self):
        '''Last update to the alert (datetime object)'''
        ts = self._ts_parse(self._raw['updated'])
        return ts

    @property
    def effective(self):
        '''Effective timestamp of the alert (datetime object)'''
        ts = self._ts_parse(self._raw['cap:effective'])
        return ts

    @property
    def published(self):
        '''Published timestamp of the alert (datetime object)'''
        ts = self._ts_parse(self._raw['published'])
        return ts

    @property
    def severity(self):
        '''Severity of alert i.e. minor, major, etc'''
        return self._raw['cap:severity']

    @property
    def category(self):
        '''Category of alert i.e. Met, Civil, etc'''
        return self._raw['cap:category']

    @property
    def urgency(self):
        '''Alert urgency'''
        return self._raw['cap:urgency']


if __name__ == '__main__':
    testdata = {'cap:expires': u'2012-10-20T07:00:00-06:00',
                'updated': u'2012-10-19T16:17:00-06:00',
                'locations': [{'state': 'ID', 'code': '016055', 'local': 'Kootenai'},
                              {'state': 'ID', 'code': '016061', 'local': 'Lewis'},
                              {'state': 'ID', 'code': '016069', 'local': 'Nez Perce'}],
                'cap:category': u'Met',
                'title': u'Wind Advisory issued October 19 at 4:17PM MDT until October 20 at 8:00PM MDT by NWS',
                'cap:certainty': u'Likely',
                'cap:severity': u'Minor',
                'cap:status': u'Actual',
                'cap:event': u'Wind Advisory',
                'cap:msgType': u'Alert',
                'cap:urgency': u'Expected',
                'cap:areaDesc': u"Coeur d'Alene Area; Lewis and Southern Nez Perce Counties",
                'published': u'2012-10-19T16:17:00-06:00',
                'cap:effective': u'2012-10-19T16:17:00-06:00',
                'summary': '''...WIND ADVISORY IN EFFECT FROM 5 AM TO 7 PM PDT SATURDAY... THE NATIONAL WEATHER SERVICE IN SPOKANE HAS ISSUED A WIND ADVISORY...WHICH IS IN EFFECT FROM 5 AM TO 7 PM PDT SATURDAY. * WINDS: SOUTHWEST 25 TO 35 MPH WITH GUSTS UP TO 45 MPH. * TIMING: WINDS WILL STEADILY INCREASE EARLY SATURDAY MORNING AND SHOULD PEAK AROUND MIDDAY.''',
                'id': '''http://alerts.weather.gov/cap/wwacapget.php?x=ID124CCA3406C4.WindAdvisory.124CCA41E2D0ID.OTXNPWOTX.24f377e1f6ddc33ee84995f226f90bb5''',
                'samecodes': ['016055',
                             '016061',
                             '016069'],

                }

    alert = Alert(testdata)
    print alert.summary
