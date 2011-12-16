#!/usr/bin/env python

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




from __future__ import print_function
import sys
import os
from time import sleep
from weatheralerts import nws



def monitor_alert_by_county(reqcounty='', reqstate=''):
    if reqcounty == '' or reqstate == '':
        print("No Location Provided")
        exit()
    req_location = { 'county': reqcounty, 'state': reqstate }

    while True:
        try:
            alerts = nws.Alerts()
            alerts.activefor_county(req_location)
            result = alerts.activefor_county(req_location)
            os.system('cls' if os.name=='nt' else 'clear')
            print(result)
            sleep(30)
        except KeyboardInterrupt:
            print("  ........Exiting.")
            sys.exit()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        monitor_alert_by_county(reqcounty=sys.argv[1], reqstate=sys.argv[2])
    else:
        print("Specify County State, see wiki for help")
