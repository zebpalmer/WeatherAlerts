from geo import GeoDB
from alert import Alert
from xml.dom import minidom


class CapParser(object):
    '''
    Parses the xml from the alert feed, creates and returns a list of alert objects.

    FIXME: the cap() method of this class needs optimization, it's slow.

    '''
    def __init__(self, raw_cap, geo=None):
        self._raw_cap = raw_cap
        if geo is None:
            self.geo = GeoDB()
        else:
            self.geo = geo
        self.samecodes = self.geo.samecodes
        self._cap_tags = ['title', 'id', 'updated', 'published', 'link', 'summary', 'cap:event', 'cap:effective',
                          'cap:expires', 'cap:status', 'cap:msgType', 'cap:category', 'cap:urgency', 'cap:severity',
                          'cap:certainty', 'cap:areaDesc', 'cap:geocode']

    def get_alerts(self):
        '''
        Public method that parses
        '''
        emptyfeed = "There are no active watches, warnings or advisories"
        alerts = []
        if emptyfeed in str(self._raw_cap):
            return alerts
        main_dom = minidom.parseString(self._raw_cap)
        xml_entries = main_dom.getElementsByTagName('entry')
        # title is currently first so we can detect an empty cap feed

        for dom in xml_entries:
            #parse the entry to a temp 'entry' dict
            entry = self._parse_entry(dom)

            # perform some cleanup before creating an object
            entry['locations'] = self.build_locations(entry)
            entry['target_areas'] = self.build_target_areas(entry)

            alert = Alert(entry)
            alerts.append(alert)
            del entry
            del alert

        return alerts

    def _parse_entry(self, dom):
        entry = {}
        for tag in self._cap_tags:
            try:
                # we need to handle the geocodes a bit differently
                if tag == 'cap:geocode':
                    try:
                        #pull out a list of SAMEcodes
                        entry['samecodes'] = str(dom.getElementsByTagName('value')[0].firstChild.data).split(' ')
                    except AttributeError:
                        entry['samecodes'] = []
                    try:
                        # pull out a list of county codes
                        entry['countycodes'] = str(dom.getElementsByTagName('value')[1].firstChild.data).split(' ')
                    except AttributeError:
                        entry['countycodes'] = []
                else:
                    try:
                        entry[tag] = dom.getElementsByTagName(tag)[0].firstChild.data
                        if entry['title'] == "There are no active watches, warnings or advisories":
                            return {}
                    except AttributeError:
                        pass
            except IndexError:
                return {}
        return entry

    def build_target_areas(self, entry):
        '''Cleanup the raw target areas description string'''
        target_areas = []
        areas = str(entry['cap:areaDesc']).split(';')
        for area in areas:
            target_areas.append(area.strip())
        return target_areas

    def build_locations(self, entry):
        '''Given an alert dict, builds location dicts'''
        locations = []
        for geo in entry['samecodes']:
            try:
                location = self.samecodes[geo]
            except KeyError:
                location = {'code': geo,
                            'local': geo,
                            'state': 'unknown'}
            locations.append(location)
        return locations


if __name__ == '__main__':
    pass
