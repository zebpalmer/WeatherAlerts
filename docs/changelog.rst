===============
Release Changes
===============

Current Development is on the 5.0 version

**0.5.0** (*in progress, not yet released*)
* 100% Test Coverage
* building python3 version at install, no longer maintaining separate code
* complete rewrite
* improved API organization
* improved documentation
* relicensed under LGPLv3
* supporting county codes



**v0.4.9** (*Current Release*)

* Last of the 4.x branch
* rather large changes to classes
* still running v0.4.5 in python2 installs will update that in 0.4.8 which will begin a release canidate for v0.5.0


Older Versions
================

Versions prior to 0.4.9 are no longer supported. It is suggest you test and upgrade to 0.5.0 when availible.


**v0.4.5**

* minor packaging changes
* added initial support for object reload based on age

**v0.4.4**

* Reorganized for easier packaging
* Supporting both Python2 and Python3 in the installer
* tox automated virtenv & tests for python 2.6, 2.7, 3.2
* Added command line monitoring script

**v0.4.1**

* Changing project name to better fit PyPi
* Packaging as an installable module


**v0.4**

* Added basic nose test script
* Refactored classes
* Added Alerts() class
* Optional json output (getting ready for web service/api)
* Various code cleanup/improvements


**v0.3.1**

* bugfix only


**v0.3:**

* refactored nagios plugin, it now uses (only) SAME code(s)
* Moved SAME code related methods to new class which can be used without parsing an alerts feed.


**v0.2:**

* moved master branch to python 3.x
* maintaining python2.x branch

**v0.1:**

* First tagged release
