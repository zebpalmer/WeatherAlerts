from geo import GeoDB
from feed import AlertsFeed
from alert import Alert

class WeatherAlerts(object):
    '''
    WeatherAlerts object that controls interaction with the samecodes and capparser classes/methods.
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
        #self.output = FormatAlerts()
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
        self.cap = AlertsFeed(state=self.scope, geo=self.geo)
        #FIXME: need to rework the handoff from the feed to the main object
        #       as part of this refactor
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


    ###def target_area(self, locations):
        ###'''
        ###TODO: not used yet
        ###sets target areas to be used in all limiting functions
        ###'''
        ###self.targetareas = locations


    ###@property
    ###def json(self):
        ###'''returns json object of all alerts on specified feed (National feed by default)'''
        ###alerts = self.cap.alerts
        ###jsonobj = self.output.jsonout(alerts)
        ###return jsonobj


    ###@property
    ###def pyobj(self):
        ###'''returns python object of all alerts for specified feed(National by default)'''
        ###if self.geocodes:
            ###alerts = self.cap.alerts

        ###alerts = self.cap.alerts
        ###jsonobj = self.output.jsonout(alerts)


    ###def national_summary(self):
        ###cap = AlertsFeed(state='US')
        ###activealerts = cap.alerts
        ###self.output.print_summary(activealerts)


    ###def state_summary(self, state=''):
        ###'''print all alerts for a given state'''
        ###if state == '':
            ###state = self.state
        ###alert_data = self.cap.alerts
        ###self.output.print_summary(alert_data)


    ###def alerts_by_samecodes(self, geocodes):
        ###'''returns alerts for a given SAME code'''
        ###cap = AlertsFeed(state='US')
        ###activealerts = cap.alerts
        ###location_alerts = []
        ###for alert in activealerts.keys():
            ###for location in activealerts[alert]['locations']:
                ###if location['code'] in geocodes:
                    ###location_alerts.append(activealerts[alert])
        ###return location_alerts


    ###def alerts_by_county_state(self, req_location):
        ###'''returns alerts for given county, state'''
        ###alert_data = self.cap.alerts
        ###county = req_location['local']
        ###state = req_location['state']
        ###location_alerts = []
        ###for alert in alert_data.keys():
            ###for location in  alert_data[alert]['locations']:
                ###if location['state'] == str(state) and location['local'] == str(county):
                    ###location_alerts.append(alert_data[alert])
        ###return location_alerts


    ###def summary(self):
        ###alert_data = self.cap.alerts
        ###alert_summary = {}
        ###if len(alert_data) == 0:
            ###return {}
        ###else:
            ###for item in alert_data:
                ###item = alert_data[item]
                ###alertareas = item['locations']
                ###a_type = item['type']
                ###for area in alertareas:
                    ###if a_type not in alert_summary:
                        ###alert_summary[a_type] = list()
                    ###if area not in alert_summary[a_type]:
                        ###alert_summary[a_type].append(area)
        ###return alert_summary

####----------------------------------------------------

    ###def alerts_by_state(self, alert_data, state):
        ###location_alerts = []
        ###for alert in alert_data.keys():
            ###for location in alert_data[alert]['locations']:
                ###if location['state'] == state:
                    ###location_alerts.append(alert_data[alert])
        ###return location_alerts

    ####@property
    ####def active_locations(self, alert_data):
        ####'''returns list of all active locations'''
        ####warned_areas = {}
        ####for alert in alert_data.keys():
            ####for location in alert_data[alert]['locations']:
                ####if location['code'] not in list(warned_areas.keys()):
                    ####warned_areas[location['code']] = [alert]
                ####else:
                    ####warned_areas[location['code']].append(alert)
        ####return warned_areas


###def alert_type(alert):
    ###'''return alert type for a given alert'''
    ###title = alert['title']
    ###a_type = title.split('issued')[0].strip()
    ###return a_type

