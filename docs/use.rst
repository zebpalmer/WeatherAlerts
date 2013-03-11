
Using WeatherAlerts
********************


Simple example
===============
This are three examples of the simplest implementation, import the WeatherAlerts class, create an instance requesting
alerts for an area based on one or more SAMECODES or bt requesting an entire State.

.. code-block:: python

   from weatheralerts import WeatherAlerts

   # Alerts by a Samecode
   nws = WeatherAlerts(samecodes='016027')
   for alert in nws.alerts:
       print alert.title

   # Alerts for a list of Samecodes
   nws = WeatherAlerts(samecodes=['016027','016001','016073','016075'])
   for alert in nws.alerts:
       print alert.title

   # Alerts for a State
   nws = WeatherAlerts(state='ID')
   for alert in nws.alerts:
       print "{0}:  {1}".format(alert.areadesc, alert.title)