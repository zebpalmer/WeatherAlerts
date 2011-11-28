#!/usr/bin/env python

'''

    This file is part of pyForecaster, this program is free software:
    you can redistribute it and/or modify it under the terms of the
    GNU General Public License as published by the Free Software
    Foundation, either version 3 of the License, or (at your option)
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''



import os
import sys
import re
import requests
from xml.dom import minidom
import simplejson
from datetime import datetime, date, timedelta
import cPickle as pickle

class CapAlerts(object):
    def __init__(self, state='US'):
        self.state = state
        self._load_same_codes()
        self._load_alerts()


    def set_state(self, state='US'):
        self.state = state
        self._load_alerts()


    def reload_alerts(self):
        print "Reloading Alerts"
        self._load_alerts(reload=True)

    def _cached_alertobj(self, reload=False):
        file = './cache/alerts_%s.cache' % (self.state)
        if os.path.exists(file):
            now = datetime.now()
            maxage = now - timedelta(minutes=5)
            file_ts = datetime.fromtimestamp(os.stat(file).st_mtime)
            if file_ts > maxage:
                cache = open(file, 'rb')
                alerts = pickle.load(cache)
                cache.close()
            else:
                print "Alerts cache is old"
                alerts = None
        else:
            print "No Alerts cache availible"
            alerts = None
        return alerts

    def _load_alerts(self, reload=False):
        if reload == True:
            self._alerts = self._parse_cap(self._get_nws_feed())
        elif reload == False:
            cached = self._cached_alertobj()
            if cached == None:
                print "Loading from web"
                self._alerts = self._parse_cap(self._get_nws_feed())
                print "Done"
            else:
                self._alerts = cached
                print "Loaded alerts from cache"


    def _get_same_codes(self):
        '''get SAME codes, load into a dict and cache'''
        same = {}
        url = '''http://www.nws.noaa.gov/nwr/SameCode.txt'''
        r = requests.get(url)
        file = r.content.split('\n')
        for line in file:
            try:
                code, local, state = line.split(',')
                location = {}
                location['code'] = code
                location['local'] = local
                location['state'] = state
                same[code] = location
            except ValueError:
                pass
        file = './cache/samecodes.cache'
        cache = open(file, 'wb')
        pickle.dump(same, cache)
        cache.close()
        return same


    def _load_same_codes(self, reload=False):
        if reload == True:
            self._get_same_codes()
        else:
            cached = self._cached_same_codes()
            if cached == None:
                self.same = self._get_same_codes()

    def _cached_same_codes(self):
        file = './cache/samecodes.cache'
        if os.path.exists(file):
            now = datetime.now()
            maxage = now - timedelta(minutes=4320)
            file_ts = datetime.fromtimestamp(os.stat(file).st_mtime)
            if file_ts > maxage:
                cache = open(file, 'rb')
                self.same = pickle.load(cache)
                cache.close()
                print "Loaded SAME codes from Cache"
                return True
            else:
                print "SAME codes cache is old, refreshing from web"
                return None
        else:
            print "No SAME codes cache availible, loading from web"
            return None



    def _get_nws_feed(self):
            '''get nws alert feed, and cache it'''
            url = '''http://alerts.weather.gov/cap/%s.php?x=0''' % (self.state)
            r = requests.get(url)
            self._feedstatus = r.status_code
            return r.content

    def _parse_cap(self, xmlstr):
        main_dom = minidom.parseString(xmlstr)

        xml_entries = main_dom.getElementsByTagName('entry')
        tags = ['title', 'updated', 'published', 'id', 'summary', 'cap:effective', 'cap:expires', 'cap:status',
                'cap:msgType', 'cap:category', 'cap:urgency', 'cap:severity', 'cap:certainty', 'cap:areaDesc',
                'cap:geocode']

        entry_num = 0
        alerts = {}
        p = re.compile('(.*) issued')
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
            entry['type'] = p.match(entry['title']).group(1)
            locations = []
            for geo in entry['geocodes']:
                try:
                    location = self.same[geo]
                except KeyError:
                    location = { 'code': geo,
                                 'local': geo,
                                 'state': 'unknown'}
                locations.append(location)
            target_areas = []
            areas = str(entry['cap:areaDesc']).split(';')
            for area in areas:
                target_areas.append(area.strip())
            entry['locations'] = locations
            entry['target_areas'] = target_areas
            alerts[entry_num] = entry
            del entry
        file = './cache/alerts_%s.cache' % (self.state)
        cache = open(file, 'wb')
        pickle.dump(alerts, cache)
        cache.close()
        return alerts


    def _alerts_summary(self):
        alert_summary = {}
        alert_data = self._alerts
        for item in alert_data:
            alertareas = alert_data[item]['locations']
            type = alert_data[item]['type']
            for area in alertareas:
                if type not in alert_summary:
                    alert_summary[type] = list()
                alert_summary[type].append(area)
        return alert_summary

    alert_summary = property(_alerts_summary)

    def print_alerts_summary(self):
        if len(self.alert_summary) == 0:
            print "No active alerts for specified area: '%s'" % (self.state)
        for key in self.alert_summary.iterkeys():
            print key + ":"
            for value in self.alert_summary[key]:
                print '\t%s county, %s' % (value['local'], value['state'])

    def summary(self, alert_data):
        alert_summary = {}
        if len(alert_data) == 0:
            return {}
        else:
            for item in alert_data:
                alertareas = item['locations']
                type = item['type']
                for area in alertareas:
                    if type not in alert_summary:
                        alert_summary[type] = list()
                    if area not in alert_summary[type]:
                        alert_summary[type].append(area)
        return alert_summary


    def print_summary(self, alerts):
            if len(alerts) == 0:
                print "No active alerts for specified area: '%s'" % (sys.argv[2])
            for key in alerts.iterkeys():
                print key + ":"
                for value in alerts[key]:
                    print '\t%s county, %s' % (value['local'], value['state'])

    def print_alertobj(self, alert_data):
        if alert_data == []:
            print "No alerts"
        else:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(alert_data)

    def print_alerts(self, alert_data):
        if alert_data == []:
            print "No Active Alerts"
        for alert in alert_data:
            print '\n'
            print alert['title']
            print '\t' + alert['summary']


    def alerts_by_county_state(self, county, state):
        location_alerts = []
        for alert in self._alerts.iterkeys():
            for location in  self._alerts[alert]['locations']:
                if location['state'] == state and location['local'] == county:
                    location_alerts.append(self._alerts[alert])
        return location_alerts


    def alerts_by_state(self, state):
            location_alerts = []
            for alert in self._alerts.iterkeys():
                for location in self._alerts[alert]['locations']:
                    if location['state'] == state:
                        location_alerts.append(self._alerts[alert])
            return location_alerts


    def _active_locations(self):
        warned_areas = {}
        for alert in self._alerts.iterkeys():
            for location in self._alerts[alert]['locations']:
                if location['code'] not in warned_areas.keys():
                    warned_areas[location['code']] = [alert]
                else:
                    warned_areas[location['code']].append(alert)
        return warned_areas
    active_areas = property(_active_locations)



if __name__ == "__main__":
    #if len(sys.argv) > 1:
        #type = sys.argv[1]
        #if type == 'summary':
            #cap = CapAlerts()
            #cap.print_alerts_summary()
        #if type == 'location':
            #cap = CapAlerts(state=sys.argv[3])
            #cap.print_alerts(cap.alerts_by_county_state(sys.argv[2], sys.argv[3]))
        #if type == 'state':
            #cap = CapAlerts(state=sys.argv[2])
            #cap.print_summary(cap.summary(cap.alerts_by_state(sys.argv[2])))

    import cProfile
    import pstats
    cProfile.run("cap=CapAlerts()", 'Cap')
    p = pstats.Stats('Cap')
    p.sort_stats('time').print_stats(20)


