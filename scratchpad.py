#!/usr/bin/env python


from time import sleep
#from weatheralerts import WeatherAlerts
from weatheralerts import WebApp




if __name__ == "__main__":
    nws_ws = WebApp()
    nws_ws.start()


    #nws = WeatherAlerts(state='ID', cachetime=1)
    #for alert in nws.alerts:
        #print "{0}:  {1}".format(alert.areadesc, alert.title)

    #nws = WeatherAlerts(cachetime=1)
    #print len(nws.alerts)
    #print len(nws.alerts)
    #sleep(70)
    #nws.refresh(force=True)
    #print len(nws.alerts)
