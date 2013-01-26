#!/usr/bin/env python



from weatheralerts import WeatherAlerts





if __name__ == "__main__":
      nws = WeatherAlerts(state='ID')
      for alert in nws.alerts:
         print "{0}:  {1}".format(alert.areadesc, alert.title)