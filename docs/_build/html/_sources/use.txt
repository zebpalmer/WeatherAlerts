Using WeatherAlerts
===================

Use cases
--------------

"WeatherAlerts was originally started as just an module/api to get and interact with the National Weather Service Alerts Feed and that remains the primary use case. 
That is, using this module to incorperate the NWS Alerts into other python programs. I will show later in the documentation how to easily to that."

The secondary purpose of this project is to provide some interaction with this data.

* A Plugin for use in Nagios (or similar monitoring server), to monitor and notify when alerts are issued
* A Command Line program that shows active alerts and refreshes every couple of minutes
* An API/Webservice build to wrap this project and provide the data in a restful webservice. 
* Desktop Plasmoid/Widget for KDE


.. toctree::
   :maxdepth: 2

   api
   nagios
   command_line
   
