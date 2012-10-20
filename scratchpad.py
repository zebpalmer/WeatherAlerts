#!/usr/bin/env python



from weatheralerts import WeatherAlerts








if __name__ == "__main__":
    nws = WeatherAlerts()
    samealerts = nws.samecode_alerts('030081')
    for alert in samealerts:
        print alert.event