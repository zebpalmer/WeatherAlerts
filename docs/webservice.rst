*********************
Webservice
*********************


.. Note::
   Release 0.5.0 will include a webservice that will interact with WeatherAlerts and provde a RESTful api which will
   provide json data. I will also be offering a live version of this API for experimentation.





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
          "status": "ok",
          "data_timestamp": "data_timestamp",
          "alerts": [ " list of alerts"]
      }










