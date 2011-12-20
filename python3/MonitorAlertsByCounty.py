#!/usr/bin/env python3

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




import sys
import os
from time import sleep
from weatheralerts import nws



def monitor_alert_by_county(reqcounty='', reqstate=''):
    if reqcounty == '' or reqstate == '':
        print("No Location Provided")
        exit()
    req_location = { 'local': reqcounty, 'state': reqstate }
    print("Loading Alerts")

    while True:
        try:
            nws_alerts = nws.Alerts(state=reqstate)
            active_alerts = nws_alerts.alerts_by_county_state(req_location)
            if len(active_alerts) == 0:
                active_summary = "\n\tNo Alerts for {0}, {1}".format(reqcounty, reqstate)
            else:
                active_summary = nws_alerts.output.print_titles(active_alerts)
            os.system('cls' if os.name=='nt' else 'clear')
            print('\n\t'+ active_summary)
            print("\n\nPress CTRL+C to Exit")
            sleep(30)
        except KeyboardInterrupt:
            print("  ........Exiting.")
            sys.exit()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        monitor_alert_by_county(reqcounty=sys.argv[1], reqstate=sys.argv[2])
    else:
        print("Specify County State, see wiki for help")
