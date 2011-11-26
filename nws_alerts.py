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
        self._samecodes = self.cached_same()
        self.load_alerts()


    def load_alerts(self):
        self._alerts = self.parse_cap(self.cached_raw_alerts(self.state)['content'])


    def get_same_codes(self):
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


    def cached_same(self, reload=False):
        if reload == True:
            same = get_same_codes()
        else:
            file = './cache/samecodes.cache'
            if os.path.exists(file):
                now = datetime.now()
                maxage = now - timedelta(minutes=4320)
                file_ts = datetime.fromtimestamp(os.stat(file).st_mtime)
                if file_ts > maxage:
                    print "Loaded SAME codes from Cache"
                    cache = open(file, 'rb')
                    same = pickle.load(cache)
                    cache.close()

                else:
                    print "SAME codes cache is old, refreshing from web"
                    same = self.get_same_codes()
            else:
                print "No SAME codes cache availible, loading from web"
                same = self.get_same_codes()
        return same


    def get_nws_alerts(self):
            '''get nws alert feed, and cache it'''
            feed = {}
            url = '''http://alerts.weather.gov/cap/%s.php?x=0''' % (self.state)
            r = requests.get(url)
            feed['status'] = r.status_code
            feed['content'] = r.content
            file = './cache/alertsfeed_%s.cache' % (self.state)
            cache = open(file, 'wb')
            pickle.dump(feed, cache)
            cache.close()
            return feed


    def cached_raw_alerts(self, reload=False):
        if reload == True:
            feed = self.get_nws_alerts()
        else:
            file = './cache/alertsfeed_%s.cache' % (self.state)
            if os.path.exists(file):
                now = datetime.now()
                maxage = now - timedelta(minutes=3)
                file_ts = datetime.fromtimestamp(os.stat(file).st_mtime)
                if file_ts > maxage:
                    print "Loaded raw_alerts from Cache"
                    cache = open(file, 'rb')
                    feed = pickle.load(cache)
                    cache.close()

                else:
                    print "Alerts cache is old, refreshing from web"
                    feed = self.get_nws_alerts()
            else:
                print "No alerts cache availible, loading from web"
                feed = self.get_nws_alerts()

        return feed


    def parse_cap(self, xmlstr):
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
                    location = self._samecodes[geo]
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


    #def active_locations():
        #location_alerts = []
        #for alert in self._alerts.iterkeys():
            #for location in  self._alerts[alert]['locations']:
                #print location


if __name__ == "__main__":
    cap = CapAlerts()
    if len(sys.argv) > 1:
        type = sys.argv[1]
        if type == 'summary':
            cap.print_alerts_summary()
        if type == 'location':
            cap.print_alerts(cap.alerts_by_county_state(sys.argv[2], sys.argv[3]))
        if type == 'state':
            cap.print_summary(cap.summary(cap.alerts_by_state(sys.argv[2])))
