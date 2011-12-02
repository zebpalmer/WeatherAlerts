#!/usr/bin/env python



### proof of concept only at the moment, would like to add user options to set nagios status levels based on alert type
### need to add that, as well as the location below to a settings file. 



from sys import exit
from nws_alerts import CapAlerts

## Enter your state abbreviation as well as your county (same code not supported yet)

state = 'ID' 
county = 'Canyon'
samecode = ''

def location(state, county='', samecode=''):
    # not the most elegant way to do this, but this is mostly a place
    # holder as we will support multiple locations, and other location 
    # features soon
    local = {}
    if not county or samecode:
        print "Must set County or SAME code"
        exit(3)
    if len(samecode) == 6:
        local['same'] = samecode
        local['state'] = state
        local['type'] = 'samecode'
    else:
        local['county'] = county
        local['state'] = state
        local['type'] = 'county'
    return local
        


def check_alerts(location):
    if location['type'] == 'county':
        cap = CapAlerts(location['state'])
        alerts = cap.alerts_by_county_state(location['county'], location['state'])
        if len(alerts) == 0:
            print "No active alerts"
            exit(0)
        elif len(alerts) == 1:
            print cap.alerts.alerts_type()
        else:
            #print "{0} Alerts".format(len(alerts))
            types = []
            for alert in alerts:
                type = cap.alert_type(alert)
                if type not in types:
                    types.append(type)
            for type in types:
                print type + ',',
        exit(1)
        
            
            
    elif location['type'] == 'same':
        print "Not yet supported"
        exit(3)






if __name__ == "__main__":
    check_alerts(location(state, county, samecode))








