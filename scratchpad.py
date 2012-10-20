#!/usr/bin/env python



from weatheralerts import WeatherAlerts








if __name__ == "__main__":
    nws = WeatherAlerts(state='ID')
    nws.load_alerts()