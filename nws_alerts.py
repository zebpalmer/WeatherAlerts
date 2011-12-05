#!/usr/bin/env python

'''
    Project home: git.zebpalmer.com/nws-alerts     
    Original Author: Zeb Palmer   (www.zebpalmer.com)
    For more info, please see the README.txt

    This program is free software you can redistribute it and
    or modify it under the terms of the GNU General Public License 
    as published by the Free Software Foundation, either version 
    3 of the License, or (at your option) any later version.

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
from datetime import datetime, timedelta
import cPickle as pickle

class CapAlerts(object):
    def __init__(self, state='US'):
        self.state = state
        self.same = ''
        self.cachetime = 3
        self._load_same_codes()
        self._load_alerts()
        self._feedstatus = ''

    def set_maxage(self, maxage=3):
        self.cachetime = maxage


    def set_state(self, state='US'):
        self.state = state
        self._load_alerts()


    def reload_alerts(self):
        #print "Reloading Alerts"
        self._load_alerts(refresh=True)

    def _cached_alertobj(self):
        f = './cache/alerts_%s.cache' % (self.state)
        if os.path.exists(f):
            now = datetime.now()
            maxage = now - timedelta(minutes=self.cachetime)
            file_ts = datetime.fromtimestamp(os.stat(f).st_mtime)
            if file_ts > maxage:
                cache = open(f, 'rb')
                alerts = pickle.load(cache)
                cache.close()
            else:
                #print "Alerts cache is old"
                alerts = None
        else:
            #print "No Alerts cache availible"
            alerts = None
        return alerts

    def _load_alerts(self, refresh=False):
        if refresh == True:
            self.alerts = self._parse_cap(self._get_nws_feed())
        elif refresh == False:
            cached = self._cached_alertobj()
            if cached == None:
                #print "Loading from web"
                self.alerts = self._parse_cap(self._get_nws_feed())
                #print "Done"
            else:
                self.alerts = cached
                #print "Loaded alerts from cache"


    def _get_same_codes(self):
        '''get SAME codes, load into a dict and cache'''
        same = {}
        url = '''http://www.nws.noaa.gov/nwr/SameCode.txt'''
        r = requests.get(url)
        f = r.content.split('\n')
        for line in f:
            try:
                code, local, state = line.split(',')
                location = {}
                location['code'] = code
                location['local'] = local
#when I contacted the nws to add a missing same code
#they added a space before the state in the samecodes file
#stripping it out
                location['state'] = state.strip() 
                same[code] = location
            except ValueError:
                pass
        f = './cache/samecodes.cache'
        cache = open(f, 'wb')
        pickle.dump(same, cache)
        cache.close()
        return same


    def _load_same_codes(self, refresh=False):
        if refresh == True:
            self._get_same_codes()
        else:
            cached = self._cached_same_codes()
            if cached == None:
                self.same = self._get_same_codes()

    def _cached_same_codes(self):
        f = './cache/samecodes.cache'
        if os.path.exists(f):
            now = datetime.now()
            maxage = now - timedelta(minutes=4320)
            file_ts = datetime.fromtimestamp(os.stat(f).st_mtime)
            if file_ts > maxage:
                cache = open(f, 'rb')
                self.same = pickle.load(cache)
                cache.close()
                #print "Loaded SAME codes from Cache"
                return True
            else:
                #print "SAME codes cache is old, refreshing from web"
                return None
        else:
            #print "No SAME codes cache availible, loading from web"
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
        f = './cache/alerts_%s.cache' % (self.state)
        cache = open(f, 'wb')
        pickle.dump(alerts, cache)
        cache.close()
        return alerts


    def _alerts_summary(self):
        alert_summary = {}
        alert_data = self.alerts
        for item in alert_data:
            alertareas = alert_data[item]['locations']
            a_type = alert_data[item]['type']
            for area in alertareas:
                if a_type not in alert_summary:
                    alert_summary[a_type] = list()
                alert_summary[a_type].append(area)
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
                a_type = item['type']
                for area in alertareas:
                    if a_type not in alert_summary:
                        alert_summary[a_type] = list()
                    if area not in alert_summary[a_type]:
                        alert_summary[a_type].append(area)
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
            print alert['title']
            print '\t' + alert['summary']


    def alerts_by_county_state(self, county, state):
        location_alerts = []
        for alert in self.alerts.iterkeys():
            for location in  self.alerts[alert]['locations']:
                if location['state'] == str(state) and location['local'] == str(county):
                    location_alerts.append(self.alerts[alert])
        return location_alerts


    def alerts_by_state(self, state):
        location_alerts = []
        for alert in self.alerts.iterkeys():
            for location in self.alerts[alert]['locations']:
                if location['state'] == state:
                    location_alerts.append(self.alerts[alert])
        return location_alerts


    def _active_locations(self):
        warned_areas = {}
        for alert in self.alerts.iterkeys():
            for location in self.alerts[alert]['locations']:
                if location['code'] not in warned_areas.keys():
                    warned_areas[location['code']] = [alert]
                else:
                    warned_areas[location['code']].append(alert)
        return warned_areas
    active_areas = property(_active_locations)

    def alert_type(self, alert):
        title = alert['title']
        a_type = title.split('issued')[0].strip()
        return a_type




if __name__ == "__main__":
    if len(sys.argv) > 1:
        type = sys.argv[1]
        if type == 'summary':
            cap = CapAlerts()
            cap.print_alerts_summary()
        if type == 'location':
            cap = CapAlerts(state=sys.argv[3])
            cap.print_alerts(cap.alerts_by_county_state(sys.argv[2], sys.argv[3]))
        if type == 'state':
            cap = CapAlerts(state=sys.argv[2])
            cap.print_summary(cap.summary(cap.alerts_by_state(sys.argv[2])))
    else:
        print "No arguments supplied" 
