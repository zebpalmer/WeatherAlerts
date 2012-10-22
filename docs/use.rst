
Using WeatherAlerts
********************

Use cases
------------------
.. Note::
   The previous examples no longer work with the rewritten module. New examples will be added prior to release.



Simple example
===============
This is the simplest example, import the WeatherAlerts class, create an instance. We then request all alert event types for a given samecode.

.. code-block:: python

   from weatheralerts import WeatherAlerts

   nws = WeatherAlerts()
   alerts = nws.samecode_alerts('030081')
   for alert in alerts:
       print alert.event
