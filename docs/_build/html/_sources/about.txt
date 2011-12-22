About WeatherAlerts
*********************

This python module started as part of another project of mine. But since this is more useful as a standalone module, I've decided to move it to it's own project and open source it. As this is a alpha/beta release aspects of the project will change, and probably pretty often. Check back here for updates, if you install using pip, you can run ``pip install -U weatheralerts`` to get the latest version. (I've been releasing on average a minor release per week, and several point releases per week.)

Since this project gets it's data from the National Weather Service XML/CAP feed, it's free and straight from the source. Other library's I've seen (or written) get data from 3rd parties that require an API key which in many cases requires a subscription or imposes restrictions.   

This code is provided under GPLv3 (see LICENSE.txt). If you do make improvements, please contribute back to this project. I certainly welcome new features, improvments and of course bug fixes. You can submit a git pull request or email me: zeb@zebpalmer.com

This project lives at `github.com/zebpalmer/WeatherAlerts <http://github.com/zebpalmer/WeatherAlerts>`_  For current documentation, visit the `Wiki <http://github.com/zebpalmer/WeatherAlerts/wiki/Home>`_


Install
========
You can download and install via PIP by runing:  ``pip install -U weatheralerts``


Python 2 Support
=================
Development of this program is done in Python 3. However the installer now supports python 2 and with each major/minor revision release I'll backport changes to the python2 code base. 
I'm currently building and testing for Python 2.6, 2.7 and 3.2. Essentially, it should work on anything 2.6 or newer. 


Bugs & Feature Requests
========================
I'm pretty new to the python world. This is my first publicly released package, that and it's still alpha, so it's got some rough edges. If you find one, please visit the `issue tracker <http://github.com/zebpalmer/WeatherAlerts/issues>`_ and let me know. 


Goals
======
Use cases that I am in the process of supporting.  

- Command line usage (mostly done)
- Packaged module to call from other programs (working, some features to add) 
- Daemon to run and post alerts to console as they come in (done)
- Nagios monitoring script (working, but lots of features to add)
- A web service that given various paramaters will return json or raw text summaries of the requested data. (not started)
- Would love to see someone (or me when I get time/figure out how) write a KDE plasmoid/widget from this... (one day...)


*If you have another use case, feel free to submit a request and jump in to help if you can.*


Author
=======
This progam is maintained by Zeb Palmer, a Linux Systems Engineer and Professional Photographer who writes a bit of python at work and play. 
Circle me on Google Plus `zebpalmer.com/+ <http://zebpalmer.com/+>`_ and see my other work at `ZebPalmer.com <http://www.zebpalmer.com>`_



