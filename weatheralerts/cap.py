# pylint: disable=W0403
from geo import GeoDB
from alert import Alert
from xml.dom import minidom


class CapParser(object):
    '''
    Parses the xml from the alert feed, creates and returns a list of alert objects.

    FIXME: This is slow, messy, and painful to look at. I'll be totally rewriting it shortly.

    '''
    def __init__(self, raw_cap, geo=None):
        self._raw_cap = raw_cap
        if geo is not None:
            self.geo = geo
        else:
            self.geo = GeoDB()
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
            pass
        else:
            main_dom = minidom.parseString(self._raw_cap)
            xml_entries = main_dom.getElementsByTagName('entry')
            # title is currently first so we can detect an empty cap feed

            for dom in xml_entries:
                #parse the entry to a temp 'entry' dict
                entry = self._parse_entry(dom)

                # perform some cleanup before creating an object
                #entry['locations'] = self.build_locations(entry) # FIXME: remove?
                entry['target_areas'] = self.build_target_areas(entry)

                alert = Alert(entry)
                alerts.append(alert)
                del entry
                del alert

        return alerts

    def _parse_entry(self, dom):
        '''Sigh....'''
        entry = {}
        for tag in self._cap_tags:
            # we need to handle the geocodes a bit differently
            if tag == 'cap:geocode':
                try:
                    geotypes = []
                    # FIXME: this will parse VTEC and add it to the feed as well, that's both a feature and a bug
                    for item in dom.getElementsByTagName('valueName'):
                        geotypes.append(str(item.firstChild.data))
                    n = 0
                    for geotype in geotypes:
                        try:
                            entry[geotype] = str(dom.getElementsByTagName('value')[n].firstChild.data).split(' ')
                        except AttributeError:
                            pass
                        n = n + 1
                finally:
                    try:
                        entry['samecodes'] = entry['FIPS6']  # backward compatibility till refactor complete
                    except Exception:
                        entry['samecodes'] = []
            else:
                try:
                    entry[tag] = dom.getElementsByTagName(tag)[0].firstChild.data
                except AttributeError:
                    entry[tag] = ''
        return entry

    def build_target_areas(self, entry):
        '''Cleanup the raw target areas description string'''
        target_areas = []
        areas = str(entry['cap:areaDesc']).split(';')
        for area in areas:
            target_areas.append(area.strip())
        return target_areas
