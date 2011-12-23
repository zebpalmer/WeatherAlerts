#!/usr/bin/env python2

'''
    Project home: github.com/zebpalmer/WeatherAlerts
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
from urllib import urlopen as urlopen
from xml.dom import minidom
from datetime import datetime, timedelta
import pickle as pickle
import tempfile
import json
from io import open



class SameCodes(object):
    u'''SameCodes Class downloads/caches the samecodes list into an object'''
    def __init__(self):
        self.samecodes = u''
        self._cachedir = unicode(tempfile.gettempdir()) + u'/'
        self._same_cache_file = self._cachedir + u'nws_samecodes.cache'
        self._load_same_codes()


    def getcodes(self):
        u'''public method to return the same codes list'''
        return self.samecodes

    def getstate(self, geosame):
        u'''Return the state of a given SAME code'''
        state = self.samecodes[geosame][u'state']
        return state


    def getfeedscope(self, geocodes):
        u'''Given multiple SAME codes, this determines if they are all in one state if so, it returns that state.
           Otherwise it returns 'US'. This is used to determine which NWS feed needs to be parsed to get
           all alerts for the given SAME codes'''

        states = self._get_states_from_samecodes(geocodes)
        if len(states) >= 2:
            return u'US'
        else:
            return states[0]


    def _get_states_from_samecodes(self, geocodes):
        u'''Returns all states for a given list of SAME codes'''
        states = []
        for code in geocodes:
            try:
                state = self.samecodes[code][u'state']
            except KeyError:
                if not isinstance(geocodes, list):
                    print u"specified geocodes must be list"
                    raise
                else:
                    print u"SAMECODE Not found"
            if state not in states:
                states.append(state)
        return states

    def reload(self):
        u'''force refresh of Same Codes (mainly for testing)'''
        self._load_same_codes(refresh=True)


    def _load_same_codes(self, refresh=False):
        u'''Loads the Same Codes into this object'''
        if refresh == True:
            self._get_same_codes()
        else:
            cached = self._cached_same_codes()
            if cached == None:
                self.samecodes = self._get_same_codes()


    def _get_same_codes(self):
        u'''get SAME codes, load into a dict and cache'''
        same = {}
        url = u'''http://www.nws.noaa.gov/nwr/SameCode.txt'''
        codes_file = urlopen(url)
        for row in codes_file.readlines():
            try:
                code, local, state = unicode(row, u"utf-8").strip().split(u',')
                location = {}
                location[u'code'] = code
                location[u'local'] = local
                #when I contacted the nws to add a missing same code
                #they added a space before the state in the samecodes file
                #stripping it out
                location[u'state'] = state.strip()
                same[code] = location
            except ValueError:
                pass
        cache = open(self._same_cache_file, u'wb')
        pickle.dump(same, cache)
        cache.close()
        return same


    def _cached_same_codes(self):
        u'''If a cached copy is availible, return it'''
        cache_file = self._same_cache_file
        if os.path.exists(cache_file):
            now = datetime.now()
            maxage = now - timedelta(minutes=4320)
            file_ts = datetime.fromtimestamp(os.stat(cache_file).st_mtime)
            if file_ts > maxage:
                try:
                    cache = open(cache_file, u'rb')
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



class CapAlertsFeed(object):
    u'''Class to fetch and load the NWS CAP/XML Alerts feed for the US or a single state if requested
       if an instance of the SameCodes class has already been (to do a geo lookup), you can pass that
       as well to save some processing'''
    def __init__(self, state=u'US', same=None):
        self.state = state
        self._cachedir = unicode(tempfile.gettempdir()) + u'/'
        self._same_cache_file = self._cachedir + u'nws_samecodes.cache'
        self._alert_cache_file = self._cachedir + u'nws_alerts_%s.cache' % (self.state)
        if same == None:
            self.same = SameCodes()
        else:
            self.same = same
        self.samecodes = self.same.getcodes()
        self.alerts = u''
        self._cachetime = 3
        self._load_alerts()
        self._feedstatus = u''
        self.output = FormatAlerts(self)



    def set_maxage(self, maxage=3):
        u'''Override the default max age for the alerts cache'''
        self._cachetime = maxage


    def set_state(self, state=u'US'):
        u'''switch to a new state without creating a new instance'''
        self.state = state
        self._alert_cache_file = self._cachedir + u'self.alerts_%s.cache' % (self.state)
        self._load_alerts()


    def reload_alerts(self):
        u'''Reload alerts bypassing cache'''
        self._load_alerts(refresh=True)

    def _cached_alertobj(self):
        u'''If a recent cache exists, return it'''
        if os.path.exists(self._alert_cache_file):
            now = datetime.now()
            maxage = now - timedelta(minutes=self._cachetime)
            file_ts = datetime.fromtimestamp(os.stat(self._alert_cache_file).st_mtime)
            if file_ts > maxage:
                try:
                    cache = open(self._alert_cache_file, u'rb')
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
        u'''Load the alerts feed and parse it'''
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


    def _get_nws_feed(self):
        u'''get nws alert feed, and cache it'''
        url = u'''http://alerts.weather.gov/cap/%s.php?x=0''' % (self.state)
        feed = urlopen(url)
        xml = feed.read()
        return xml

    def _parse_cap(self, xmlstr):
        u'''parse the feed contents'''
        main_dom = minidom.parseString(xmlstr)

        xml_entries = main_dom.getElementsByTagName(u'entry')
        tags = [u'title', u'updated', u'published', u'id', u'summary', u'cap:effective', u'cap:expires', u'cap:status',
                u'cap:msgType', u'cap:category', u'cap:urgency', u'cap:severity', u'cap:certainty', u'cap:areaDesc',
                u'cap:geocode']

        entry_num = 0
        alerts = {}
        pat = re.compile(u'(.*) issued')
        for dom in xml_entries:
            entry_num = entry_num + 1
            entry = {}
            for tag in tags:
                try:
                    if tag == u'cap:geocode':
                        try:
                            entry[u'geocodes'] = unicode(dom.getElementsByTagName(u'value')[0].firstChild.data).split(u' ')
                        except AttributeError:
                            entry[u'geocodes'] = []
                    else:
                        try:
                            entry[tag] = dom.getElementsByTagName(tag)[0].firstChild.data
                            if entry[u'title'] == u"There are no active watches, warnings or advisories":
                                return {}
                        except AttributeError:
                            pass
                except IndexError:
                    return {}
            entry[u'type'] = pat.match(entry[u'title']).group(1)
            locations = []
            for geo in entry[u'geocodes']:
                try:
                    location = self.samecodes[geo]
                except KeyError:
                    location = { u'code': geo,
                                 u'local': geo,
                                 u'state': u'unknown'}
                locations.append(location)
            target_areas = []
            areas = unicode(entry[u'cap:areaDesc']).split(u';')
            for area in areas:
                target_areas.append(area.strip())
            entry[u'locations'] = locations
            entry[u'target_areas'] = target_areas
            alerts[entry_num] = entry
            del entry
        cache = open(self._alert_cache_file, u'wb')
        pickle.dump(alerts, cache)
        cache.close()
        return alerts


    def _alerts_summary(self):
        alert_summary = {}
        alert_data = self.alerts
        for item in alert_data:
            alertareas = alert_data[item][u'locations']
            a_type = alert_data[item][u'type']
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
                alertareas = item[u'locations']
                a_type = item[u'type']
                for area in alertareas:
                    if a_type not in alert_summary:
                        alert_summary[a_type] = list()
                    if area not in alert_summary[a_type]:
                        alert_summary[a_type].append(area)
        return alert_summary


    def alerts_by_county_state(self, county, state):
        u'''returns alerts for given county, state'''
        location_alerts = []
        for alert in self.alerts.keys():
            for location in  self.alerts[alert][u'locations']:
                if location[u'state'] == unicode(state) and location[u'local'] == unicode(county):
                    location_alerts.append(self.alerts[alert])
        return location_alerts


    def alerts_by_samecodes(self, geocodes):
        u'''returns alerts for a given SAME code'''
        location_alerts = []
        for alert in self.alerts.keys():
            for location in  self.alerts[alert][u'locations']:
                if location[u'code'] in geocodes:
                    location_alerts.append(self.alerts[alert])
        return location_alerts


    def alerts_by_state(self, state):
        location_alerts = []
        for alert in self.alerts.keys():
            for location in self.alerts[alert][u'locations']:
                if location[u'state'] == state:
                    location_alerts.append(self.alerts[alert])
        return location_alerts


    def _active_locations(self):
        warned_areas = {}
        for alert in self.alerts.keys():
            for location in self.alerts[alert][u'locations']:
                if location[u'code'] not in list(warned_areas.keys()):
                    warned_areas[location[u'code']] = [alert]
                else:
                    warned_areas[location[u'code']].append(alert)
        return warned_areas
    active_areas = property(_active_locations)

    def alert_type(self, alert):
        title = alert[u'title']
        a_type = title.split(u'issued')[0].strip()
        return a_type



class FormatAlerts(object):
    def __init__(self, cap, alerts=u''):
        self.cap = cap


    def print_alerts_summary(self):
        outstr = u''
        if len(self.cap.alert_summary.keys()) == 0:
            outstr = u"No active alerts for specified area: '%s'" % (self.cap.feed)
        else:
            for key in self.cap.alert_summary.keys():
                outstr = outstr + key + u":" + u'\n'
                for value in self.cap.alert_summary[key]:
                    outstr = outstr + u'\t%s county, %s' % (value[u'local'], value[u'state']) + u'\n'
        return outstr


    def print_summary(self, alerts):
        if len(alerts) == 0:
            print u"No active alerts for specified area: '%s'" % (sys.argv[2])
        for key in alerts.keys():
            print key + u":"
            for value in alerts[key]:
                print u'\t%s county, %s' % (value[u'local'], value[u'state'])


    def print_alertobj(self, alert_data):
        if alert_data == []:
            print u"No alerts"
        else:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(alert_data)

    def alerts(self, alert_data):
        outstr = u''
        if alert_data == []:
            outstr = u"No Active Alerts"
        else:
            for alert in alert_data:
                outstr = outstr + (alert[u'title'])
                outstr = outstr + (u'\t' + alert[u'summary'])
        return outstr


    def jsonout(self, alerts):
        jsonobj = json.dumps(alerts)
        return jsonobj


class Alerts(object):
    def __init__(self):
        pass


    def national_summary(self):
        cap = CapAlertsFeed(state=u'US')
        outstr = cap.output.print_alerts_summary()
        return outstr


    def state_summary(self, state):
        cap = CapAlertsFeed(state=state)
        cap.output.print_alerts_summary()


    def activefor_county(self, location, formatout=u'print'):
        cap = CapAlertsFeed(location[u'state'])
        alerts = cap.alerts_by_county_state(location[u'county'], location[u'state'])
        if formatout == u'print':
            strout = cap.output.alerts(alerts)
        elif formatout == u'json':
            strout = cap.output.jsonout(alerts)
        return strout


    def activefor_samecodes(self, geocodes, formatout=u'print'):
        geocodes = geocodes.split(u',')
        same = SameCodes()
        scope = same.getfeedscope(geocodes)
        cap = CapAlertsFeed(state=scope, same=same)
        alerts = cap.alerts_by_samecodes(geocodes)
        if formatout == u'print':
            strout = cap.output.alerts(alerts)
        elif formatout == u'json':
            strout = cap.output.jsonout(alerts)
        return strout



if __name__ == u"__main__":
    if len(sys.argv) > 1:
        nwsalerts = Alerts()
        req_type = sys.argv[1]
        if req_type == u'summary':
            result = nwsalerts.national_summary()
        if req_type == u'location':
            req_location = { u'county': sys.argv[2], u'state': sys.argv[3]}
            result = nwsalerts.activefor_county(req_location)
        if req_type == u'state':
            result = nwsalerts.state_summary(state=sys.argv[2])
        if req_type == u'samecodes':
            result = nwsalerts.activefor_samecodes(sys.argv[2])

        print result
    else:
        print u"No arguments supplied"
