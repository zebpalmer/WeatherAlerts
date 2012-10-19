from weatheralerts import GeoDB


class CapParser(object):
    def __init__(self, capxml, geo=None):
        if geo is None:
            self.geo = GeoDB()
        else:
            self.geo = geo
        self.samecodes = self.geo.samecodes
        self.parse_cap(capxml)

    def parse_cap(self, xmlstr):
        '''parse and cache the feed contents'''
        main_dom = minidom.parseString(xmlstr)

        xml_entries = main_dom.getElementsByTagName('entry')
        tags = ['title', 'updated', 'published', 'id', 'summary', 'cap:effective', 'cap:expires', 'cap:status',
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
            tmp_alerts[entry_num] = entry
            del entry
        return tmp_alerts
