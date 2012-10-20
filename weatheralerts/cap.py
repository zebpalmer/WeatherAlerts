from geo import GeoDB
from alert import Alert
from xml.dom import minidom
import re

class CapParser(object):
    '''
    Parses the xml from the alert feed, creates and returns a list of alert objects.

    FIXME: the _parse_cap() method of this class needs optimization, it's slow.

    NOTE: This class has no public methods and just returns a list, it'll probably be moved
    or refactored into a function as the rewrite continues
    '''
    def __init__(self, geo=None):
        if geo is None:
            self.geo = GeoDB()
        else:
            self.geo = geo
        self.samecodes = self.geo.samecodes


    def cap(self, raw_cap):
        alerts = []
        main_dom = minidom.parseString(raw_cap)

        xml_entries = main_dom.getElementsByTagName('entry')
        # title is currently first so we can detect "an empty cap feed
        tags = ['title', 'id', 'updated', 'published', 'link', 'summary', 'cap:event', 'cap:effective', 'cap:expires', 'cap:status',
                'cap:msgType', 'cap:category', 'cap:urgency', 'cap:severity', 'cap:certainty', 'cap:areaDesc',
                'cap:geocode']

        entry_num = 0
        tmp_alerts = {}
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
                    location = {'code': geo,
                                'local': geo,
                                'state': 'unknown'}
                locations.append(location)

            target_areas = []
            areas = str(entry['cap:areaDesc']).split(';')
            for area in areas:
                target_areas.append(area.strip())
            entry['locations'] = locations
            entry['target_areas'] = target_areas
            alert = Alert(entry)
            alerts.append(alert)
            del entry
            del alert

        return alerts


if __name__ == '__main__':
    pass