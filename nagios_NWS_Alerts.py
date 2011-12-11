#!/usr/bin/env python



### proof of concept only at the moment, would like to add user options to set nagios status levels based on alert type
### need to add that, as well as the location below to a settings file.



from sys import exit, argv
from nws_alerts import nws_alerts



def check_alerts(alerts):
    if len(alerts) == 0:
        print("No active alerts")
        exit(0)
    elif len(alerts) == 1:
        print(cap.alerts.alerts_type())
    else:
        #print "{0} Alerts".format(len(alerts))
        types = []
        for alert in alerts:
            alert_type = cap.alert_type(alert)
            if alert_type not in types:
                types.append(alert_type)
        for alert_type in types:
            print(alert_type + ',', end=' ')
    exit(1)


def loadalerts(geocodes):
    geocodes = geocodes.split(',')
    same = nws_alerts.SameCodes()
    scope = same.getfeedscope(geocodes)
    cap = nws_alerts.CapAlerts(state=scope, same=same)
    alerts = cap.alerts_by_samecodes(geocodes)    
    check_alerts(alerts)



if __name__ == "__main__":
    if len(argv) != 2:
        print ('''Please specify the SAME code(s) for the area(s) you wish to check
\tSee http://www.nws.noaa.gov/nwr/indexnw.htm for help finding your SAME area.
\tSeparate multiple same codes by commas with no spaces''') 
        exit(3)
    else:
        loadalerts(argv[1])






