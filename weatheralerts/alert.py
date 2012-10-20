from dateutil.parser import parse
from datetime import datetime



class Alert():
    def __init__(self, cap_dict):
        '''
        Create an alert object with the cap dict created from cap xml parser.
        This object won't do much, mostly a bunch of propery methods to sanitize
        and generally muck around with the raw dict. We put off all that processing
        until it's actually needed.
        '''
        self._raw = cap_dict


    def _ts_parse(self, ts):
        dt = parse(ts)
        return dt

    @property
    def expiration(self):
        ts = self._ts_parse(self._raw['cap:expires'])
        return ts


    @property
    def updated(self):
        ts = self._ts_parse(self._raw['updated'])
        return ts

    @property
    def effective(self):
        ts = self._ts_parse(self._raw['cap:effective'])
        return ts

    @property
    def published(self):
        ts = self._ts_parse(self._raw['published'])
        return ts

    @property
    def severity(self):
        return self._raw['cap:severity']

    @property
    def category(self):
        return self._raw['cap:category']


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
                'summary': u'...WIND ADVISORY IN EFFECT FROM 5 AM TO 7 PM PDT SATURDAY... THE NATIONAL WEATHER SERVICE IN SPOKANE HAS ISSUED A WIND ADVISORY...WHICH IS IN EFFECT FROM 5 AM TO 7 PM PDT SATURDAY. * WINDS: SOUTHWEST 25 TO 35 MPH WITH GUSTS UP TO 45 MPH. * TIMING: WINDS WILL STEADILY INCREASE EARLY SATURDAY MORNING AND SHOULD PEAK AROUND MIDDAY.',
                'type': u'Wind Advisory',
                'id': u'http://alerts.weather.gov/cap/wwacapget.php?x=ID124CCA3406C4.WindAdvisory.124CCA41E2D0ID.OTXNPWOTX.24f377e1f6ddc33ee84995f226f90bb5',
                'geocodes': ['016055',
                             '016061',
                             '016069']}

    alert = Alert(testdata)
    print alert.expiration













