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
from weatheralerts import nws



if __name__ == "__main__":
    if len(sys.argv) > 1:
        req_type = sys.argv[1]
        if req_type == 'summary':
            nws_alerts = nws.Alerts()
            result = nws_alerts.output.print_summary(nws_alerts.summary())
        elif req_type == 'location':
            req_location = { 'local': sys.argv[2], 'state': sys.argv[3]}
            nws_alerts = nws.Alerts(state=req_location['state'])
            active_alerts = nws_alerts.alerts_by_county_state(req_location)
            if len(active_alerts) == 0:
                result = "No Active Alerts"
            else:
                result = nws_alerts.output.print_titles(active_alerts)
        elif req_type == 'state':
            nws_alerts = nws.Alerts(state=sys.argv[2])
            result = nws_alerts.output.print_summary(nws_alerts.summary())

        elif req_type == 'samecodes':
            #result = nws_alerts.activefor_samecodes(sys.argv[2])
            req_geocodes = sys.argv[2].split(',')
            nws_alerts = nws.Alerts(geocodes=req_geocodes)
            active_alerts = nws_alerts.alerts_by_samecodes(req_geocodes)
            if len(active_alerts) == 0:
                result = "No Active Alerts"
            else:
                result = nws_alerts.output.print_titles(active_alerts)

        print(result)
    else:
        print("No arguments supplied, please see the wiki")
