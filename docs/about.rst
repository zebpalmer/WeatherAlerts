About WeatherAlerts
*********************

This python module started as part of another project of mine. But since this is more useful as a standalone module, I've decided to move it to it's own project and open source it. As this is a alpha/beta release aspects of the project will change, and probably pretty often. Check back here for updates, if you install using pip, you can run ``pip install -U weatheralerts`` to get the latest version. (I've been releasing on average a minor release per week, and several point releases per week.)

Since this project gets it's data from the National Weather Service XML/CAP feed, it's free and straight from the source. Other library's I've seen (or written) get data from 3rd parties that require an API key which in many cases requires a subscription or imposes restrictions.

This code is provided under LGPLv3 as of version 0.5a (see LICENSE.txt). If you do make improvements, please contribute back to this project. You can submit a git pull request or email me: zeb@zebpalmer.com

This project lives at `github.com/zebpalmer/WeatherAlerts <http://github.com/zebpalmer/WeatherAlerts>`_

Install
========
You can download and install the current stable version via PIP by runing:  ``pip install -U weatheralerts``

Alternativly you can download and install directly from the source code on github.



Bugs & Feature Requests
========================
When you find one, please report it in the `issue tracker <http://github.com/zebpalmer/WeatherAlerts/issues>`_


Goals
======
Use cases that I am in considering in the development of WeatherAlerts.

- Simple command line tool for checking active, local alerts.
- Packaged module to call from other programs
- Daemon to run and notify alerts as they come in
- Nagios monitoring pluging
- A web service that given various paramaters will return json or raw text summaries of the requested data.
- Would love to see someone a KDE plasmoid/widget that would pop up alerts




Author
=======
This progam is maintained by Zeb Palmer, a Linux Systems Engineer and Professional Photographer who writes a bit of
python at work and play. Circle me on Google Plus `zebpalmer.com/+ <http://zebpalmer.com/+>`_ and see my other work at
`ZebPalmer.com <http://www.zebpalmer.com>`_

Contact
==========

There are several ways you can contact me or otherwise get help beyond the documentation.

**Bug Reports**
  Please submit bug reports via the projects issue tracker on github https://github.com/zebpalmer/WeatherAlerts/issues

**Feature Requests**
  You can submit an issue via the above link or email me zeb@zebpalmer.com

**Random Chatter**
  Circle me on Google+ `Zeb Palmer Google Plus <https://plus.google.com/u/0/105137345884947048400/>`_
  Follow me on Twitter `@zebpalmer <http://twitter.com/zebpalmer>`_

**Website**
  For info on other projects, see my website, `Zeb Palmer <http://www.zebpalmer.com>`_

