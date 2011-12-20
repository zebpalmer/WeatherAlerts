#!/usr/bin/env python3

import sys
from weatheralerts import nws



if __name__ == "__main__":
    if len(sys.argv) > 1:
        nwsalerts = nws.Alerts()
        req_type = sys.argv[1]
        if req_type == 'summary':
            alert_data = nwsalerts.summary()
            result = nwsalerts.output.print_summary(alert_data)
        if req_type == 'location':
            req_location = { 'county': sys.argv[2], 'state': sys.argv[3]}
            result = nwsalerts.activefor_county(req_location)
        if req_type == 'state':
            result = nwsalerts.state_summary(state=sys.argv[2])
        if req_type == 'samecodes':
            result = nwsalerts.activefor_samecodes(sys.argv[2])

        print(result)
    else:
        print("No arguments supplied, please see the wiki")