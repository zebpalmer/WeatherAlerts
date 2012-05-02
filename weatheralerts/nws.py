#!/usr/bin/env python3

'''
WeatherAlerts.nws
*******************

File Information
==================

**Project Home:**
  http://github.com/zebpalmer/WeatherAlerts

**Original Author:**
  Zeb Palmer http://www.zebpalmer.com


**Documentation:**
  http://weatheralerts.readthedocs.org


**License:**
  GPLv3 - full text included in LICENSE.txt


License Notice:
"""""""""""""""""
This program is free software you can redistribute it and or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.  You should have received a copy of the GNU General Public
License along with this program. If not, see <http://www.gnu.org/licenses/>.


Code Documentation
===================

'''



import os
import sys
import re
try:
    from urllib import request
except:
    from urllib import urlopen as request
    print("You are trying to run the python3 version in python2, this won't go well")
from xml.dom import minidom
from datetime import datetime, timedelta
import pickle as pickle
import tempfile
import json



class GeoDB(object):
    '''Interact with samecodes object and other geolocation data that will be added soon'''
    def __init__(self):
        self.__same = SameCodes()
        self.samecodes = self.__same.samecodes


    def location_lookup(self, req_location):
        '''
        returns full location given samecode or county and state. Returns False if not valid.
        *currently locations are a dictionary, once other geo data is added, they will move to a location class/obj*
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
        '''Given County, State return the SAME code for specified location. Return False if not found'''
        for location in self.samecodes:
            if state == self.samecodes[location]['state']:
                if local == self.samecodes[location]['local']:
                    return self.samecodes[location]
        return False

    def getstate(self, geosame):
        '''Given a SAME code, return the state that SAME code is in'''
        state = self.samecodes[geosame]['state']
        return state


    def getfeedscope(self, geocodes):
        '''Given multiple SAME codes, determine if they are all in one state. If so, it returns that state.
           Otherwise return 'US'. This is used to determine which NWS feed needs to be parsed to get
           all alerts for the requested SAME codes'''
        states = self.get_states_from_samecodes(geocodes)
        if len(states) >= 2:
            return 'US'
        else:
            return states[0]


    def get_states_from_samecodes(self, geocodes):
        '''Returns all states for a given list of SAME codes
        *Shouldn't be used to determine feed scope, please use getfeedscope()*

        '''
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



#### GET/PARSE SAME CODES TABLE ##############################################################

class SameCodes(object):
    '''
    Is used to download, parse and cache the SAME codes data from the web.
    *All interaction with the SAME codes data should be done in the GeoGB classy*
    '''
    def __init__(self):
        self._cachedir = str(tempfile.gettempdir()) + '/'
        self._same_cache_file = self._cachedir + 'nws_samecodes.cache'
        self._load_same_codes()

    @property
    def samecodes(self):
        '''public method to return the same codes list'''
        return self._samecodes


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
                self._samecodes = self._get_same_codes()


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
                    self._samecodes = pickle.load(cache)
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


#### FEED PARSER #######################################################################################################

class CapAlertsFeed(object):
    '''Class to fetch and load the NWS CAP/XML Alerts feed for the US or a single state if requested
       if an instance of the SameCodes class has already been (to do a geo lookup), you can pass that
       as well to save some processing'''
    def __init__(self, state='US', geo=None, maxage=3, reload=False):
        self._alerts = ''
        self._feedstatus = ''
        self._cachetime = maxage
        self.state = self._set_state(state, refresh=False)
        self._cachedir = str(tempfile.gettempdir()) + '/'
        self._alert_cache_file = self._cachedir + 'nws_alerts_%s.cache' % (self.state)
        if geo == None:
            self.geo = GeoDB()
        else:
            self.geo = geo
        self.samecodes = self.geo.samecodes

        self._cachetime = 3
        self._alerts_ts = datetime.now()
        self._lookuptable = {}
        self._reload = reload
        # now for the real work
        self._load_alerts()
        


    @property
    def alerts(self):
        '''returns all alerts on feed'''
        self.check_objectage()
        return self._alerts


    def _set_state(self, state, refresh=True):
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
            self._alerts = self._parse_cap(self._get_nws_feed())
        elif refresh == False:
            cached = self._cached_alertobj()
            if cached == None:
                self._alerts = self._parse_cap(self._get_nws_feed())
            else:
                self._alerts = cached


    def _get_nws_feed(self):
        '''get nws alert feed, and cache it'''
        url = '''http://alerts.weather.gov/cap/%s.php?x=0''' % (self.state)
        feed = request.urlopen(url)
        xml = feed.readall()
        return xml

    def _parse_cap(self, xmlstr):
        '''parse and cache the feed contents'''
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

                # We're going to create a table to reference alerts by
                # TODO: make all alert lookups use the resulting data 
                self._create_lookuptable(geo, entry_num, entry['type'])

            target_areas = []
            areas = str(entry['cap:areaDesc']).split(';')
            for area in areas:
                target_areas.append(area.strip())
            entry['locations'] = locations
            entry['target_areas'] = target_areas
            alerts[entry_num] = entry
            del entry
        # cache alerts data
        cache = open(self._alert_cache_file, 'wb')
        pickle.dump(alerts, cache)
        cache.close()
        self._alerts_ts = datetime.now()
        return alerts

    def _create_lookuptable(self, samecode, alert_num, alert_type):
        alert_tuple = (alert_num, alert_type)
        if samecode in self._lookuptable:
            self._lookuptable[samecode].append(alert_tuple)
        else:
            _alertids = []
            _alertids.append(alert_tuple)
            self._lookuptable[samecode] = _alertids
    

class FormatAlerts(object):
    def __init__(self):
        pass


    def print_summary(self, alert_data):
        strout = ''
        if len(alert_data) == 0:
            strout = "No active alerts for specified area: '%s'" % (sys.argv[2])
        for key in alert_data.keys():
            strout = strout + key + ":\n"
            for value in alert_data[key]:
                strout = strout + '\t%s county, %s\n' % (value['local'], value['state'])
        return strout



    def print_titles(self, alert_data):
        strout = ''
        for alert in alert_data:
            strout = strout + alert['title'] + '\n'
        return strout


    def print_obj(self, alert_data):
        if alert_data == []:
            print("No alerts")
        else:
            import pprint
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(alert_data)

    def print_alerts(self, alert_data):
        outstr = ''
        if alert_data == []:
            outstr = "No Active Alerts"
        else:
            for alert in alert_data:
                outstr = outstr + (alert['title'])
                outstr = outstr + ('\t' + alert['summary'])
        return outstr


    def jsonout(self, alert_data):
        '''dump given alerts to json'''
        jsonobj = json.dumps(alert_data)
        return jsonobj


class Alerts(object):
    '''
    Alerts object that controls interaction with the samecodes and capparser classes/methods.
    Pass state='' or geocodes='samecodes_list' to change which feed is being parsed
    passing a list of samecodes will determine if they are in the same state and pick
    the correct feed or use the US feed if they're in different states
    '''
    def __init__(self, state='', geocodes='', load=True):
        '''
        init Alerts, default to National Feed, set state or geocodes to define a feed for a given area.
        if geocodes are specified, then all alerts objects will be limited to those areas
        '''
        self.state = state
        self.geo = GeoDB()
        self.output = FormatAlerts()
        if geocodes == '':
            if self.state == '':
                self.scope = 'US'
            else:
                self.scope = state
        else:
            self.scope = self.geo.getfeedscope(geocodes)

        if load == True:
            self.load_alerts()


    def load_alerts(self):
        '''manually load the cap feed/alerts'''
        self.cap = CapAlertsFeed(state=self.scope, geo=self.geo)
        self._alerts = self.cap.alerts


    def refresh_alerts(self):
        self.cap.reload_alerts()
        self.load_alerts()


    def set_state(self, state):
        '''sets state, reloads alerts unless told otherwise'''
        if len(state) == 2:
            self.state = state.upper()
            self.scope = self.state
            self.load_alerts_from_feed()


    def target_area(self, locations):
        '''
        TODO: not used yet
        sets target areas to be used in all limiting functions
        '''
        self.targetareas = locations


    @property
    def json(self):
        '''returns json object of all alerts on specified feed (National feed by default)'''
        alerts = self.cap.alerts
        jsonobj = self.output.jsonout(alerts)
        return jsonobj


    @property
    def pyobj(self):
        '''returns python object of all alerts for specified feed(National by default)'''
        if self.geocodes:
            alerts = self.cap.alerts

        alerts = self.cap.alerts
        jsonobj = self.output.jsonout(alerts)


    def national_summary(self):
        cap = CapAlertsFeed(state='US')
        activealerts = cap.alerts
        self.output.print_summary(activealerts)


    def state_summary(self, state=''):
        '''print all alerts for a given state'''
        if state == '':
            state = self.state
        alert_data = self.cap.alerts
        self.output.print_summary(alert_data)


    def alerts_by_samecodes(self, geocodes):
        '''returns alerts for a given SAME code'''
        cap = CapAlertsFeed(state='US')
        activealerts = cap.alerts
        location_alerts = []
        for alert in activealerts.keys():
            for location in activealerts[alert]['locations']:
                if location['code'] in geocodes:
                    location_alerts.append(activealerts[alert])
        return location_alerts


    def alerts_by_county_state(self, req_location):
        '''returns alerts for given county, state'''
        alert_data = self.cap.alerts
        county = req_location['local']
        state = req_location['state']
        location_alerts = []
        for alert in alert_data.keys():
            for location in  alert_data[alert]['locations']:
                if location['state'] == str(state) and location['local'] == str(county):
                    location_alerts.append(alert_data[alert])
        return location_alerts


    def summary(self):
        alert_data = self.cap.alerts
        alert_summary = {}
        if len(alert_data) == 0:
            return {}
        else:
            for item in alert_data:
                item = alert_data[item]
                alertareas = item['locations']
                a_type = item['type']
                for area in alertareas:
                    if a_type not in alert_summary:
                        alert_summary[a_type] = list()
                    if area not in alert_summary[a_type]:
                        alert_summary[a_type].append(area)
        return alert_summary

#----------------------------------------------------

    def alerts_by_state(self, alert_data, state):
        location_alerts = []
        for alert in alert_data.keys():
            for location in alert_data[alert]['locations']:
                if location['state'] == state:
                    location_alerts.append(alert_data[alert])
        return location_alerts

    #@property
    #def active_locations(self, alert_data):
        #'''returns list of all active locations'''
        #warned_areas = {}
        #for alert in alert_data.keys():
            #for location in alert_data[alert]['locations']:
                #if location['code'] not in list(warned_areas.keys()):
                    #warned_areas[location['code']] = [alert]
                #else:
                    #warned_areas[location['code']].append(alert)
        #return warned_areas


def alert_type(alert):
    '''return alert type for a given alert'''
    title = alert['title']
    a_type = title.split('issued')[0].strip()
    return a_type










if __name__ == "__main__":
    nws_alerts = Alerts(state='ID')
