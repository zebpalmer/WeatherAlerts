#!/usr/bin/env python3

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