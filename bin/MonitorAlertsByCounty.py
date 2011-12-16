#!/usr/bin/env python
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
