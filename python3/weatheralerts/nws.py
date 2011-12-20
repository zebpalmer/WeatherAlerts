#!/usr/bin/env python3

'''
    Project home: git.zebpalmer.com/nws-alerts
    Original Author: Zeb Palmer   (www.zebpalmer.com)
    For more info, please see the README.rst

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
from urllib import request
from xml.dom import minidom
from datetime import datetime, timedelta
import pickle as pickle
import tempfile
import json



class SameCodes(object):
    '''SameCodes Class downloads/caches the samecodes list into an object'''
    def __init__(self):
        self.samecodes = ''
        self._cachedir = str(tempfile.gettempdir()) + '/'
        self._same_cache_file = self._cachedir + 'nws_samecodes.cache'
        self._load_same_codes()


    def getcodes(self):
        '''public method to return the same codes list'''
        return self.samecodes

    def getstate(self, geosame):
        '''Return the state of a given SAME code'''
        state = self.samecodes[geosame]['state']
        return state


    def getfeedscope(self, geocodes):
        '''Given multiple SAME codes, this determines if they are all in one state if so, it returns that state.
           Otherwise it returns 'US'. This is used to determine which NWS feed needs to be parsed to get
           all alerts for the given SAME codes'''

        states = self._get_states_from_samecodes(geocodes)
        if len(states) >= 2:
            return 'US'
        else:
            return states[0]


    def _get_states_from_samecodes(self, geocodes):
        '''Returns all states for a given list of SAME codes'''
        states = []
        for code in geocodes:
            try:
                state = self.samecodes[code]['state']
            except KeyError:
                if not isinstance(geocodes, list):
                    print ("specified geocodes must be list")
                    raise
                else:
                    print("SAMECODE Not found")
            if state not in states:
                states.append(state)
        return states

    def reload(self):
        '''force refresh of Same Codes (mainly for testing)'''
        self._load_same_codes(refresh=True)


    def _load_same_codes(self, refresh=False):
        '''Loads the Same Codes into this object'''
        if refresh == True:
            self._get_same_codes()
        else:
            cached = self._cached_same_codes()
            if cached == None:
                self.samecodes = self._get_same_codes()


    def _get_same_codes(self):
        '''get SAME codes, load into a dict and cache'''
        same = {}
        url = '''http://www.nws.noaa.gov/nwr/SameCode.txt'''
        codes_file = request.urlopen(url)
        for row in codes_file.readlines():
            try:
                code, local, state = str(row, "utf-8").strip().split(',')
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
        cache = open(self._same_cache_file, 'wb')
        pickle.dump(same, cache)
        cache.close()
        return same


    def _cached_same_codes(self):
        '''If a cached copy is availible, return it'''
        cache_file = self._same_cache_file
        if os.path.exists(cache_file):
            now = datetime.now()
            maxage = now - timedelta(minutes=4320)
            file_ts = datetime.fromtimestamp(os.stat(cache_file).st_mtime)
            if file_ts > maxage:
                try:
                    cache = open(cache_file, 'rb')
                    self.samecodes = pickle.load(cache)
                    cache.close()
                    #print "Loaded SAME codes from Cache"
                    return True
                except Exception:
                    # if any problems opening cache, ignore and move on
                    return None
            else:
                #print "SAME codes cache is old, refreshing from web"
                return None
        else:
            #print "No SAME codes cache availible, loading from web"
            return None


    def location_lookup(self, req_location):
        '''
        returns full location given samecode or county and state. Returns False if not valid.
        '''
        location = False
        locations = self.samecodes
        try:
            location = locations[req_location['code']]
        except KeyError:
            pass
        try:
            location = self.lookup_samecode(req_location['local'], req_location['state'])
        except KeyError:
            pass
        return location


    def lookup_samecode(self, local, state):
        '''return same code given county, state'''
        for location in self.samecodes:
            if state == self.samecodes[location]['state']:
                if local == self.samecodes[location]['local']:
                    return self.samecodes[location]

        return False


class CapAlertsFeed(object):
    '''Class to fetch and load the NWS CAP/XML Alerts feed for the US or a single state if requested
       if an instance of the SameCodes class has already been (to do a geo lookup), you can pass that
       as well to save some processing'''
    def __init__(self, state='US', same=None):
        self.alerts = ''
        self._feedstatus = ''
        self.state = self.set_state(state, refresh=False)
        self._cachedir = str(tempfile.gettempdir()) + '/'
        self._same_cache_file = self._cachedir + 'nws_samecodes.cache'
        self._alert_cache_file = self._cachedir + 'nws_alerts_%s.cache' % (self.state)
        if same == None:
            self.same = SameCodes()
        else:
            self.same = same
        self.samecodes = self.same.getcodes()
        self._cachetime = 3
        self._alerts_ts = datetime.now()
        self._load_alerts()
        #self.output = FormatAlerts(self)


    def set_maxage(self, maxage=3):
        '''Override the default max age for the alerts cache'''
        self._cachetime = maxage


    def set_state(self, state, refresh=True):
        '''sets state, reloads alerts unless told otherwise'''
        if len(state) == 2:
            self.state = state.upper()
            if refresh == True:
                self._alert_cache_file = self._cachedir + 'self.alerts_%s.cache' % (self.state)
                self._load_alerts()
            return state
        else:
            raise Exception('Error parsing given state')


    def reload_alerts(self):
        '''Reload alerts bypassing cache'''
        self._load_alerts(refresh=True)


    def check_objectage(self):
        '''check age of alerts in this object, reload if past max cache time'''
        now = datetime.now()
        maxage = now - timedelta(minutes=self._cachetime)
        if self._alerts_ts > maxage:
            self.reload_alerts()


    def _cached_alertobj(self):
        '''If a recent cache exists, return it'''
        if os.path.exists(self._alert_cache_file):
            now = datetime.now()
            maxage = now - timedelta(minutes=self._cachetime)
            file_ts = datetime.fromtimestamp(os.stat(self._alert_cache_file).st_mtime)
            if file_ts > maxage:
                try:
                    cache = open(self._alert_cache_file, 'rb')
                    alerts = pickle.load(cache)
                    cache.close()
                except Exception:
                    # if any problems loading cache file, ignore and move on
                    # (this is here to prevent issues switching between python2 and python3)
                    alerts = None
            else:
                #"Alerts cache is old"
                alerts = None
        else:
            #"No Alerts cache availible"
            alerts = None
        return alerts


    def _load_alerts(self, refresh=False):
        '''Load the alerts feed and parse it'''
        if refresh == True:
            self.alerts = self._parse_cap(self._get_nws_feed())
        elif refresh == False:
            cached = self._cached_alertobj()
            if cached == None:
                self.alerts = self._parse_cap(self._get_nws_feed())
            else:
                self.alerts = cached


    def _get_nws_feed(self):
        '''get nws alert feed, and cache it'''
        url = '''http://alerts.weather.gov/cap/%s.php?x=0''' % (self.state)
        feed = request.urlopen(url)
        xml = feed.readall()
        return xml

    def _parse_cap(self, xmlstr):
        '''parse the feed contents'''
        main_dom = minidom.parseString(xmlstr)

        xml_entries = main_dom.getElementsByTagName('entry')
        tags = ['title', 'updated', 'published', 'id', 'summary', 'cap:effective', 'cap:expires', 'cap:status',
                'cap:msgType', 'cap:category', 'cap:urgency', 'cap:severity', 'cap:certainty', 'cap:areaDesc',
                'cap:geocode']

        entry_num = 0
        alerts = {}
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
        cache = open(self._alert_cache_file, 'wb')
        pickle.dump(alerts, cache)
        cache.close()
        self._alerts_ts = datetime.now()
        return alerts

#----------------------------------------------------

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


    def alerts_by_county_state(self, county, state):
        '''returns alerts for given county, state'''
        location_alerts = []
        for alert in self.alerts.keys():
            for location in  self.alerts[alert]['locations']:
                if location['state'] == str(state) and location['local'] == str(county):
                    location_alerts.append(self.alerts[alert])
        return location_alerts


    def alerts_by_samecodes(self, geocodes):
        '''returns alerts for a given SAME code'''
        location_alerts = []
        for alert in self.alerts.keys():
            for location in  self.alerts[alert]['locations']:
                if location['code'] in geocodes:
                    location_alerts.append(self.alerts[alert])
        return location_alerts


    def alerts_by_state(self, state):
        location_alerts = []
        for alert in self.alerts.keys():
            for location in self.alerts[alert]['locations']:
                if location['state'] == state:
                    location_alerts.append(self.alerts[alert])
        return location_alerts

    @property
    def active_locations(self):
        '''returns list of all active locations'''
        warned_areas = {}
        for alert in self.alerts.keys():
            for location in self.alerts[alert]['locations']:
                if location['code'] not in list(warned_areas.keys()):
                    warned_areas[location['code']] = [alert]
                else:
                    warned_areas[location['code']].append(alert)
        return warned_areas


    def alert_type(self, alert):
        '''return alert type for a given alert'''
        title = alert['title']
        a_type = title.split('issued')[0].strip()
        return a_type



class FormatAlerts(object):
    def __init__(self, cap):
        self.cap = cap


    def print_alerts_summary(self):
        outstr = ''
        if len(self.cap.alert_summary.keys()) == 0:
            outstr = "No active alerts for specified area: '%s'" % (self.cap.feed)
        else:
            for key in self.cap.alert_summary.keys():
                outstr = outstr + key + ":" + '\n'
                for value in self.cap.alert_summary[key]:
                    outstr = outstr + '\t%s county, %s' % (value['local'], value['state']) + '\n'
        return outstr


    def print_summary(self, alerts):
        if len(alerts) == 0:
            print("No active alerts for specified area: '%s'" % (sys.argv[2]))
        for key in alerts.keys():
            print(key + ":")
            for value in alerts[key]:
                print('\t%s county, %s' % (value['local'], value['state']))


    def print_alertobj(self, alert_data):
        if alert_data == []:
            print("No alerts")
        else:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(alert_data)

    def alerts(self, alert_data):
        outstr = ''
        if alert_data == []:
            outstr = "No Active Alerts"
        else:
            for alert in alert_data:
                outstr = outstr + (alert['title'])
                outstr = outstr + ('\t' + alert['summary'])
        return outstr


    def jsonout(self, alerts):
        '''dump given alerts to json'''
        jsonobj = json.dumps(alerts)
        return jsonobj


class Alerts(object):
    def __init__(self):
        pass


    def national_summary(self):
        cap = CapAlertsFeed(state='US')
        outstr = cap.output.print_alerts_summary()
        return outstr


    def state_summary(self, state):
        '''print all alerts for a given state'''
        cap = CapAlertsFeed(state=state)
        cap.output.print_alerts_summary()


    def activefor_county(self, location, formatout='print'):
        '''display alerts for a county/state'''
        cap = CapAlertsFeed(location['state'])
        alerts = cap.alerts_by_county_state(location['county'], location['state'])
        if formatout == 'print':
            strout = cap.output.alerts(alerts)
        elif formatout == 'json':
            strout = cap.output.jsonout(alerts)
        return strout


    def activefor_samecodes(self, geocodes, formatout='print'):
        geocodes = geocodes.split(',')
        same = SameCodes()
        scope = same.getfeedscope(geocodes)
        cap = CapAlertsFeed(state=scope, same=same)
        alerts = cap.alerts_by_samecodes(geocodes)
        if formatout == 'print':
            strout = cap.output.alerts(alerts)
        elif formatout == 'json':
            strout = cap.output.jsonout(alerts)
        return strout



def test_same_lookup():
    expected = {'state': 'ID', 'code': '016027', 'local': 'Canyon'}
    same = SameCodes()
    req_location = { 'code': '016027'}
    response = same.location_lookup(req_location)
    assert response == expected

def test_county_lookup():
    expected = {'state': 'ID', 'code': '016027', 'local': 'Canyon'}
    same = SameCodes()
    req_location = {'state': 'ID', 'local': 'Canyon'}
    response = same.location_lookup(req_location)
    assert response == expected



if __name__ == "__main__":
    pass

