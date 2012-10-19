=====================
WeatherAlerts README
=====================


Please note:
===================
This project is in a state of flux, I'm rewriting it as I have time....
If you want a working copy of the code you can install via pip (See below) or download Tag 0.4.7 on github.


PROJECT STATUS & TODO
===================
This module is a mess (but mostly a functional mess) as it started in my early days of python... as I have time I'm rewriting it.
I'm dropping support for python 3 on the rewrite branch since 90% of what I code in is 2.7. I will certainly port it back to 3 before
releasing the new version to pypi. In the meantime, feel free to work on the rewrite branch, but if you want working code, stick with master.



Documentation
==============
Please see http://weatheralerts.readthedocs.org for current documentation


About
======
This python module started as part of another project of mine. But since this is more useful as a standalone module,
I've decided to move it to it's own project and open source it. As this is a alpha/beta release aspects of the project will change,
and probably pretty often. Check back here for updates, if you install using pip, you can run ``pip install -U weatheralerts`` to get the latest version.

Since this project gets it's data from the National Weather Service XML/CAP feed, it's free and straight from the source.
Other modules I've seen (or written) get data from 3rd parties that require an API key which in many cases requires a subscription or imposes restrictions on use.

This code is provided under GPLv3 (see LICENSE.txt). If you do make improvements, please contribute back to this project. I certainly welcome new features, improvments and of course bug fixes. You can submit a git pull request or email me: zeb@zebpalmer.com

This project lives at `github.com/zebpalmer/WeatherAlerts <http://github.com/zebpalmer/WeatherAlerts>`_  For current documentation, visit the online docs at http://weatheralerts.readthedocs.org/


Install
---------
You can download and install via PIP by runing:  ``pip install -U weatheralerts``


Python 2/3 Support
-----------------
The released version of this module supports recent versions of both 2.x and 3.x.



This program is maintained by Zeb Palmer, a Linux Systems Engineer and Professional Photographer wh