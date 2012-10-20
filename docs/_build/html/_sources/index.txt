=====================
WeatherAlerts Docs
=====================

.. Warning::

   **Version 0.5 (rewrite branch) will not be backwards compatibile with version 0.4 (current release)**
   This module is in alpha, it's API can and will change. New versions will likely break backwards compatibility.
   This will become more stable as we approch the 1.0 release. For now, I encourage you to test new versions with your
   program before upgrading.

.. Note::
   You're looking at documentation for the rewrite branch of WeatherAlerts. If you're looking for documentation
   for the latest stable branch (and what's currently in pypi) click `Latest <http://weatheralerts.readthedocs.org/en/latest/>`_

Welcome
----------
WeatherAlerts is a python project which interacts with the Emergency Alerts data provided free from the
National Weather Service. Feeds for each state (or a National feed) are provided in NWS CAP format, which is XML. This feed is free to the public
(supported by taxpayers) and offers an alternative to paid services which are just getting data from this feed anyway.

The project uses S.A.M.E codes, which are geocodes which the NWS uses to target alerts to specifc areas via thier National Weather Radio network.
We will be adding additional geo location methods in the future.

Please take a look through the documentation here, if you still have questions, contact me.

Current Development
.....................
The current release is availble on pypi, source code for that release can be found on githug, tagged v0.4.8


Python 2/3 Support
---------------------
The current relased version of WeatherAlerts supports both python 2 and python 3. However, current development is being done in Python 2.
When the rewrite is nearing completion, I'll port it to python 3.



Documentation Contents
--------------------------------

.. toctree::
   :maxdepth: 2

   about
   use
   devstatus
   contact
   changelog
   module

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`

