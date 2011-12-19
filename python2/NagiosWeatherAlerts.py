#!/usr/bin/env python3

u'''
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


from sys import exit, argv
from weatheralerts import nws



def check_alerts(alerts):
    if len(alerts) == 0:
        print u"No active alerts"
        statuscode = 0
    elif len(alerts) == 1:
        print cap.alerts.alerts_type()
    else:
        #print "{0} Alerts".format(len(alerts))
        types = []
        for alert in alerts:
            alert_type = cap.alert_type(alert)
            if alert_type not in types:
                types.append(alert_type)
        for alert_type in types:
            print alert_type + u',',
        statuscode = 1
    return statuscode


def loadalerts(geocodes):
    geocodes = geocodes.split(u',')
    same = nws.SameCodes()
    scope = same.getfeedscope(geocodes)
    cap = nws.CapAlertsFeed(state=scope, same=same)
    alerts = cap.alerts_by_samecodes(geocodes)    
    check_alerts(alerts)



if __name__ == u"__main__":
    if len(argv) != 2:
        print u'''Please specify the SAME code(s) for the area(s) you wish to check
\tSee http://www.nws.noaa.gov/nwr/indexnw.htm for help finding your SAME area.
\tSeparate multiple same codes by commas with no spaces''' 
        exit(3)
    else:
        statuscode = loadalerts(argv[1])
        exit(statuscode)




