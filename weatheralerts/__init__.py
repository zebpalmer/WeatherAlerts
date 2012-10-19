#!/usr/bin/env python3

'''
WeatherAlerts.nws
*******************

File Information
==================

**Project Home:**
  http://github.com/zebpalmer/WeatherAlerts

**Original Author:**
  Zeb Palmer http://www.zebpalmer.com


**Documentation:**
  http://weatheralerts.readthedocs.org


**License:**
  GPLv3 - full text included in LICENSE.txt


License Notice:
"""""""""""""""""
This program is free software you can redistribute it and or modify it under the terms of the GNU General Public
License as published by the Free Software Foundation, either version 3 of the License, or (at your option)
any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.  You should have received a copy of the GNU General Public
License along with this program. If not, see <http://www.gnu.org/licenses/>.


Code Documentation
===================

'''


import os
import sys
import re
from xml.dom import minidom
from datetime import datetime, timedelta
import pickle as pickle
import tempfile
import json

#from .feed import AlertsFeed
#from .weatheralerts import WeatherAlerts