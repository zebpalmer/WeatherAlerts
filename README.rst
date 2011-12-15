==================
NWS-ALERTS README
==================


About
======
This python module started as part of another project of mine. But since this provided additional functionality, I've decided to move it to it's own project and open source it. 

This code is provided under GPLv3 (see LICENSE.txt). If you do make improvements, please contribute back to this project. I certainly welcome new features, improvments and of course bug fixes. You can submit a git pull request or email me: zeb@zebpalmer.com

You can this project lives at `github.com/zebpalmer/WeatherAlerts <http://github.com/zebpalmer/WeatherAlerts>`_  For current documentation, visit the `Wiki <http://github.com/zebpalmer/WeatherAlerts/wiki/Home>`_

**About The Author**

Originally written by Zeb Palmer, a Linux Systems Engineer and Professional Photographer who writes a bit of python at work and play. 
Circle me on Google Plus `zebpalmer.com/+ <http://zebpalmer.com/+>`_ and see my other work at `ZebPalmer.com <http://www.zebpalmer.com>`_
 
Install
---------
You can download and install via PIP by runing ``pip install -u weatheralerts``


Python 2 Support
-----------------
The master branch and all releases of this program are written for Python 3.x. Shortly after any released version, I will update the python2.x branch, you can download and use it, but there will be no supported releases from it. 

Use
--------
Please see the wiki linked above for current use documentation. 


Goals
------
Use cases that I am moving to support first. 

- Command line usage 
- Packaged module to call from other programs 
- Nagios monitoring script 
- A web service that given various paramaters will return json or raw text summaries of the requested data.
 
*If you have another use case, feel free to submit a request and jump in to help if you can.*
