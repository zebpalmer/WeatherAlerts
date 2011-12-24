Using WeatherAlerts
********************

Use cases
--------------

WeatherAlerts was originally started as just an module/api to get and interact with the National Weather Service Alerts Feed and that remains the primary use case. 
That is, using this module to incorperate the NWS Alerts into other python programs. I will show later in the documentation how to easily to that.

The secondary purpose of this project is to provide some interaction with this data.

* A Plugin for use in Nagios (or similar monitoring server), to monitor and notify when alerts are issued
* A Command Line program that shows active alerts and refreshes every couple of minutes
* An API/Webservice build to wrap this project and provide the data in a restful webservice. 
* Desktop Plasmoid/Widget for KDE


Nagios
^^^^^^^

The example Nagios plugin does work though it needs improvement to add more configuration options. 
Currently the plugin accepts a list of SAME codes separated by comma and will result in a Nagios alert for any alert issued for the requested area. 

Additional configuration for this is planned, allowing you to specify which alert types result in what level of nagios status. 

API
^^^^^^^

If you're wanting to use this data in your project, there are a couple ways to do it. First (and recommended)
you can create the object and request the alerts data from it, transforming and interacting with it as desired.
Currently the module provides a json output that memics the CAP standard but with the addition of geodata and some
other manipulations. Second (and not recommended) you can take the formatted output from one of the output methods
and display that directly.



Command Line Tools
^^^^^^^^^^^^^^^^^^^^

Currently there are two command line tools (not counting the nagios plugin) that are included with WeatherAlerts. 

#. MonitorAlertsByCounty.py
#. NWS_Alerts.py


MonitorAlertsByCounty.py
""""""""""""""""""""""""
This script, given County and State as command line arguments, will display active alerts refreshing the feed every 2-3 minutes. 
Example: ``MonitorAlertsByCounty.py  Canyon ID`` 


NWS_Alerts.py
""""""""""""""
Is a general command line interface to the WeatherAlerts module, it allows you to query alerts based on SAMECODES, County/State as well as State and National Summaries. 
this will be documented soon, but if you look at the script it should be clear. 
