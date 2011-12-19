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




import sys
import os
from time import sleep
from weatheralerts import nws



def monitor_alert_by_county(reqcounty=u'', reqstate=u''):
    if reqcounty == u'' or reqstate == u'':
        print u"No Location Provided"
        exit()
    req_location = { u'county': reqcounty, u'state': reqstate }

    while True:
        try:
            alerts = nws.Alerts()
            alerts.activefor_county(req_location)
            result = alerts.activefor_county(req_location)
            os.system(u'cls' if os.name==u'nt' else u'clear')
            print result
            sleep(30)
        except KeyboardInterrupt:
            print u"  ........Exiting."
            sys.exit()

if __name__ == u"__main__":
    if len(sys.argv) == 3:
        monitor_alert_by_county(reqcounty=sys.argv[1], reqstate=sys.argv[2])
    else:
        print u"Specify County State, see wiki for help"
