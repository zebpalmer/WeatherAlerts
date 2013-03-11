=====================================
National Weather Service Alert Data
=====================================

Overview
------------
This package pulls in 'near realtime' alert data from the National Weather Service (NWS) CAP index feed. It's an
ATOM/XML feed with additional CAP 1.1 defined fields.




Caveats
-----------


SAME Codes and Geo Location
.............................
Currently this project makes extensive use of SAME codes, it's been noted that 'not all NWS products are issued with a
SAME Code'. However, 'County/Zone codes are provided for all CAP 1.1 messages.' I've noticed that a lot of Alaskan
alerts do not ship with SAME codes, some don't appear to ship with any geocodes... Most lower 48 alerts do, in fact,
I haven't seen one that didn't. For this reason though, we'll be incorperating county/zone codes and Storm based
location information in the near future.


Near Realtime
..............
The NWS states that the feed is updated in 'near real time', elsewhere it states that the feed is updated 'roughly every
two minutes'. It appears to me that it's somewhere in the middle, certainly being updated often enough for non immediate
life threatening alerts. If you live in an area prone to flash floods, tornados, or Tsunami's, you should be relying on
the National Weather Service Weather Radio for your primary alerting method.