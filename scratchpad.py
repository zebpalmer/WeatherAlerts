#!/usr/bin/env python



from weatheralerts import WeatherAlerts





if __name__ == "__main__":
    nws = WeatherAlerts(samecodes='016027')
    for alert in nws.alerts:
        print alert.event