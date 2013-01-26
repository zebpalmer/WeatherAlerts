
Using WeatherAlerts
********************

Use cases
------------------
.. Note::
   The previous examples no longer work with the rewritten module. New examples will be added prior to release.



Simple example
===============
This is the simplest example, import the WeatherAlerts class, create an instance. We then request all alerts for a
given samecode, list of samecodes or for a State.

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