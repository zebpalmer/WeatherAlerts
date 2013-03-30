*********************
Webservice
*********************


.. Note::
   This feature is currently only in the 'dev' branch of WeatherAlerts and has not been released to PyPI yet.
   It will be added to the 0.5.0 release which should be availible soon. This documentation is provided as a
   preview. You can try this out by downloading and installing the development branch from github.


The WeatherAlerts webservice allows you to setup a single webservice and request Severe Weather and other
Emergency Alerts from multiple clients (data is provided as JSON). This can give you some flexibility in
use as well as reducing the requests you make to the NWS servers if you are using multiple clients.


I will be offering a Live version of this webservice for experimentation in the near future, details of which will
be documented here.


Start the Webservice
----------------------

To setup a webservice that provides data for the entire US, run the code below.

.. code-block:: python

   from weatheralerts import WebApp
   nws_ws = WebApp()
   nws_ws.start()


If however, you know will only be requesting data for one state, you can save a few electrons by specifying the state.

.. code-block:: python

   from weatheralerts import WebApp
   nws_ws = WebApp(state='ID')
   nws_ws.start()




Webservice API Documentation
------------------------------


.. http:get:: /all

   Will return json data for all alerts on the feed.

   **Example request**:

   .. sourcecode:: http

      GET /all HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      {
         "webservice": {
             "status": true,
             "disclaimer": "Don't rely on this for anything important, it's for experimentation purposes only."
         },
         "alerts": []
     }


.. http:get:: /samecodes/(samecodes)

   Will return json data for alerts that match the specifed samecode(s). When requesting data for multiple samecodes,
   separate them with commas, no spaces.

   **Example request**:

   .. sourcecode:: http

      GET /samecodes/012065,013281 HTTP/1.1
      Host: example.com
      Accept: application/json, text/javascript

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Vary: Accept
      Content-Type: text/javascript

      {
         "webservice": {
             "status": true,
             "disclaimer": "Don't rely on this for anything important, it's for experimentation purposes only."
         },
         "alerts": [
             {
                 "zonecodes": [],
                 "updated": "2013-03-28T23:29:00-04:00",
                 "msgtype": "Alert",
                 "link": "http://alerts.weather.gov/cap/wwacapget.php?x=FL124EF51C78C4.FloodWarning.124EF52B3A80FL.TAEFLSTAE.285023120b4e86a12ca32387f953554e",
                 "event": "Flood Warning",
                 "category": "Met",
                 "severity": "Moderate",
                 "effective": "2013-03-28T23:29:00-04:00",
                 "title": "Flood Warning issued March 28 at 11:29PM EDT until March 29 at 8:00PM EDT by NWS",
                 "summary": "...THE FLOOD WARNING CONTINUES FOR THE FOLLOWING RIVERS IN FLORIDA... AUCILLA RIVER AT LAMONT (US 27) AFFECTING JEFFERSON...MADISON AND TAYLOR COUNTIES..",
                 "areadesc": "Jefferson; Madison; Taylor",
                 "expiration": "2013-03-29T20:00:00-04:00",
                 "published": "2013-03-28T23:29:00-04:00",
                 "samecodes": [
                     "012065",
                     "012079",
                     "012123"
                 ],
                 "urgency": "Expected"
             }
         ]
     }








