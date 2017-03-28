import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import unittest
from weatheralerts.cap import CapParser

# some sample cap xml
rc = """<?xml version = '1.0' encoding = 'UTF-8' standalone = 'yes'?>




<feed xmlns = 'http://www.w3.org/2005/Atom'
xmlns:cap = 'urn:oasis:names:tc:emergency:cap:1.1'
xmlns:ha = 'http://www.alerting.net/namespace/index_1.0'>

<id>http://alerts.weather.gov/cap/id.atom</id>
<logo>http://alerts.weather.gov/images/xml_logo.gif</logo>
<generator>NWS CAP Server</generator>
<updated>2013-01-26T13:13:00-07:00</updated>
<author>
<name>w-nws.webmaster@noaa.gov</name>
</author>
<title>Current Watches, Warnings and Advisories for Idaho Issued by the National Weather Service</title>
<link href='http://alerts.weather.gov/cap/id.atom'/>

<entry>
<id>http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE90581D4.DenseFogAdvisory.124EE911B1C0ID.BOINPWBOI.94f563b5486fa14b27263b9f27b03205</id>
<updated>2013-01-26T13:13:00-07:00</updated>
<published>2013-01-26T13:13:00-07:00</published>
<author>
<name>w-nws.webmaster@noaa.gov</name>
</author>
<title>Dense Fog Advisory issued January 26 at 1:13PM MST until January 26 at 1:00PM MST by NWS</title>
<link href="http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE90581D4.DenseFogAdvisory.124EE911B1C0ID.BOINPWBOI.94f563b5486fa14b27263b9f27b03205"/>
<summary>...DENSE FOG CONTINUES IN THE IDAHO TREASURE VALLEY... .DENSE FOG CONTINUES IN THE IDAHO PORTION OF THE LOWER TREASURE VALLEY WHERE VISIBILITY HAS BEEN LESS THAN 200 YARDS...ESPECIALLY BETWEEN CALDWELL AND BOISE. VISIBILITY SHOULD IMPROVE AS A COLD FRONT COMES THROUGH THE AREA LATE TODAY. ...DENSE FOG ADVISORY IN EFFECT UNTIL 5 PM MST THIS AFTERNOON...</summary>
<cap:event>Dense Fog Advisory</cap:event>
<cap:effective>2013-01-26T13:13:00-07:00</cap:effective>
<cap:expires>2013-01-26T17:00:00-07:00</cap:expires>
<cap:status>Actual</cap:status>
<cap:msgType>Alert</cap:msgType>
<cap:category>Met</cap:category>
<cap:urgency>Expected</cap:urgency>
<cap:severity>Minor</cap:severity>
<cap:certainty>Likely</cap:certainty>
<cap:areaDesc>Lower Treasure Valley</cap:areaDesc>
<cap:polygon></cap:polygon>
<cap:geocode>
<valueName>FIPS6</valueName>
<value>016027 016045 016073 016075 016087</value>
<valueName>UGC</valueName>
<value>IDZ012</value>
</cap:geocode>
<cap:parameter>
<valueName>VTEC</valueName>
<value>/O.EXP.KBOI.FG.Y.0008.000000T0000Z-130126T2000Z/
/O.NEW.KBOI.FG.Y.0009.130126T2013Z-130127T0000Z/</value>
</cap:parameter>
</entry>

<entry>
<id>http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE90581D4.DenseFogAdvisory.124EE911B1C0ID.BOINPWBOI.12dfa8dd949036098cfca451659153b7</id>
<updated>2013-01-26T13:13:00-07:00</updated>
<published>2013-01-26T13:13:00-07:00</published>
<author>
<name>w-nws.webmaster@noaa.gov</name>
</author>
<title>Dense Fog Advisory issued January 26 at 1:13PM MST until January 26 at 5:00PM MST by NWS</title>
<link href="http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE90581D4.DenseFogAdvisory.124EE911B1C0ID.BOINPWBOI.12dfa8dd949036098cfca451659153b7"/>
<summary>...DENSE FOG CONTINUES IN THE IDAHO TREASURE VALLEY... .DENSE FOG CONTINUES IN THE IDAHO PORTION OF THE LOWER TREASURE VALLEY WHERE VISIBILITY HAS BEEN LESS THAN 200 YARDS...ESPECIALLY BETWEEN CALDWELL AND BOISE. VISIBILITY SHOULD IMPROVE AS A COLD FRONT COMES THROUGH THE AREA LATE TODAY. ...DENSE FOG ADVISORY IN EFFECT UNTIL 5 PM MST THIS AFTERNOON...</summary>
<cap:event>Dense Fog Advisory</cap:event>
<cap:effective>2013-01-26T13:13:00-07:00</cap:effective>
<cap:expires>2013-01-26T17:00:00-07:00</cap:expires>
<cap:status>Actual</cap:status>
<cap:msgType>Alert</cap:msgType>
<cap:category>Met</cap:category>
<cap:urgency>Expected</cap:urgency>
<cap:severity>Minor</cap:severity>
<cap:certainty>Likely</cap:certainty>
<cap:areaDesc>Upper Treasure Valley</cap:areaDesc>
<cap:polygon></cap:polygon>
<cap:geocode>
<valueName>FIPS6</valueName>
<value>016001 016039 016073</value>
<valueName>UGC</valueName>
<value>IDZ014</value>
</cap:geocode>
<cap:parameter>
<valueName>VTEC</valueName>
<value>/O.NEW.KBOI.FG.Y.0009.130126T2013Z-130127T0000Z/</value>
</cap:parameter>
</entry>

<entry>
<id>http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE9056A64.FloodWatch.124EE920F400ID.MSOFFAMSO.738619c9bd434bd0bfbf7001349f0197</id>
<updated>2013-01-26T12:53:00-07:00</updated>
<published>2013-01-26T12:53:00-07:00</published>
<author>
<name>w-nws.webmaster@noaa.gov</name>
</author>
<title>Flood Watch issued January 26 at 12:53PM MST until January 27 at 5:00PM MST by NWS</title>
<link href="http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE9056A64.FloodWatch.124EE920F400ID.MSOFFAMSO.738619c9bd434bd0bfbf7001349f0197"/>
<summary>...FLOOD WATCH NOW IN EFFECT THROUGH SUNDAY AFTERNOON... THE FLOOD WATCH IS NOW IN EFFECT FOR * A PORTION OF NORTH CENTRAL IDAHO...INCLUDING THE FOLLOWING COUNTY...LEMHI. * THROUGH SUNDAY AFTERNOON * TEMPERATURES IN THE SALMON AND LEMHI VALLEYS HAVE WARMED</summary>
<cap:event>Flood Watch</cap:event>
<cap:effective>2013-01-26T12:53:00-07:00</cap:effective>
<cap:expires>2013-01-27T17:00:00-07:00</cap:expires>
<cap:status>Actual</cap:status>
<cap:msgType>Alert</cap:msgType>
<cap:category>Met</cap:category>
<cap:urgency>Future</cap:urgency>
<cap:severity>Moderate</cap:severity>
<cap:certainty>Possible</cap:certainty>
<cap:areaDesc>Lemhi</cap:areaDesc>
<cap:polygon></cap:polygon>
<cap:geocode>
<valueName>FIPS6</valueName>
<value>016059</value>
<valueName>UGC</valueName>
<value>IDC059</value>
</cap:geocode>
<cap:parameter>
<valueName>VTEC</valueName>
<value>/O.EXT.KMSO.FA.A.0002.000000T0000Z-130128T0000Z/
/00000.0.IJ.000000T0000Z.000000T0000Z.000000T0000Z.OO/</value>
</cap:parameter>
</entry>

<entry>
<id>http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE9053A58.WinterWeatherAdvisory.124EE905CAE0ID.MSOWSWMSO.67d47e7b54dd47ad8d5910a7bbb339d1</id>
<updated>2013-01-26T11:30:00-07:00</updated>
<published>2013-01-26T11:30:00-07:00</published>
<author>
<name>w-nws.webmaster@noaa.gov</name>
</author>
<title>Winter Weather Advisory issued January 26 at 11:30AM MST until January 26 at 3:00PM MST by NWS</title>
<link href="http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE9053A58.WinterWeatherAdvisory.124EE905CAE0ID.MSOWSWMSO.67d47e7b54dd47ad8d5910a7bbb339d1"/>
<summary>...WINTER WEATHER ADVISORY REMAINS IN EFFECT UNTIL 2 PM PST THIS AFTERNOON ABOVE 4500 FEET... A WINTER WEATHER ADVISORY ABOVE 4500 FEET REMAINS IN EFFECT UNTIL 2 PM PST THIS AFTERNOON. * IMPACTS/TIMING: SNOW WILL ACCUMULATE ABOVE 4500 FEET THROUGH THIS AFTERNOON. EXPECT SLICK ROADWAYS ON HIGHWAY 12 OVER LOLO</summary>
<cap:event>Winter Weather Advisory</cap:event>
<cap:effective>2013-01-26T11:30:00-07:00</cap:effective>
<cap:expires>2013-01-26T15:00:00-07:00</cap:expires>
<cap:status>Actual</cap:status>
<cap:msgType>Alert</cap:msgType>
<cap:category>Met</cap:category>
<cap:urgency>Expected</cap:urgency>
<cap:severity>Minor</cap:severity>
<cap:certainty>Likely</cap:certainty>
<cap:areaDesc>Northern Clearwater Mountains; Southern Clearwater Mountains</cap:areaDesc>
<cap:polygon></cap:polygon>
<cap:geocode>
<valueName>FIPS6</valueName>
<value>016035 016049</value>
<valueName>UGC</valueName>
<value>IDZ005 IDZ006</value>
</cap:geocode>
<cap:parameter>
<valueName>VTEC</valueName>
<value>/O.CON.KMSO.WW.Y.0008.000000T0000Z-130126T2200Z/</value>
</cap:parameter>
</entry>

<entry>
<id>http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE9053A58.WinterWeatherAdvisory.124EE905CAE0ID.MSOWSWMSO.8267d50e98191686ab5e8d4821939726</id>
<updated>2013-01-26T11:30:00-07:00</updated>
<published>2013-01-26T11:30:00-07:00</published>
<author>
<name>w-nws.webmaster@noaa.gov</name>
</author>
<title>Winter Weather Advisory issued January 26 at 11:30AM MST until January 27 at 11:00AM MST by NWS</title>
<link href="http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE9053A58.WinterWeatherAdvisory.124EE905CAE0ID.MSOWSWMSO.8267d50e98191686ab5e8d4821939726"/>
<summary>...WINTER WEATHER ADVISORY IN EFFECT FROM 2 PM THIS AFTERNOON TO 11 AM MST SUNDAY... THE NATIONAL WEATHER SERVICE IN MISSOULA HAS ISSUED A WINTER WEATHER ADVISORY FOR SNOW...WHICH IS IN EFFECT FROM 2 PM THIS AFTERNOON TO 11 AM MST SUNDAY. * IMPACTS/TIMING: SNOW...MODERATE AT TIMES...WILL DEVELOP</summary>
<cap:event>Winter Weather Advisory</cap:event>
<cap:effective>2013-01-26T11:30:00-07:00</cap:effective>
<cap:expires>2013-01-26T15:00:00-07:00</cap:expires>
<cap:status>Actual</cap:status>
<cap:msgType>Alert</cap:msgType>
<cap:category>Met</cap:category>
<cap:urgency>Expected</cap:urgency>
<cap:severity>Minor</cap:severity>
<cap:certainty>Likely</cap:certainty>
<cap:areaDesc>Eastern Lemhi County; Western Lemhi County</cap:areaDesc>
<cap:polygon></cap:polygon>
<cap:geocode>
<valueName>UGC</valueName>
<value>IDZ009 IDZ010</value>
</cap:geocode>
<cap:parameter>
<valueName>VTEC</valueName>
<value>/O.EXB.KMSO.WW.Y.0008.130126T2100Z-130127T1800Z/</value>
</cap:parameter>
</entry>

<entry>
<id>http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE90427BC.SpecialWeatherStatement.124EE905CAE0ID.PIHSPSPIH.db949cd29dd427fabcbb7cdbafe8d16a</id>
<updated>2013-01-26T04:27:00-07:00</updated>
<published>2013-01-26T04:27:00-07:00</published>
<author>
<name>w-nws.webmaster@noaa.gov</name>
</author>
<title>Special Weather Statement issued January 26 at 4:27AM MST by NWS</title>
<link href="http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE90427BC.SpecialWeatherStatement.124EE905CAE0ID.PIHSPSPIH.db949cd29dd427fabcbb7cdbafe8d16a"/>
<summary>...WIDESPREAD SNOW AND COLDER WEATHER RETURNS STARTING TONIGHT... A STORM SYSTEM WILL BEGIN AFFECTING PORTIONS OF THE CENTRAL MOUNTAINS ALONG WITH THE MAGIC VALLEY AND SOUTHERN HIGHLANDS THIS EVENING AND TONIGHT. DURING THE DAY TOMORROW...THE FOCUS QUICKLY SHIFTS TO THE SOUTHERN AND EASTERN MOUNTAINS...AS WELL AS ALONG THE INTERSTATE CORRIDORS. A COLD FRONT SWEEPS THROUGH...HELPING TO</summary>
<cap:event>Special Weather Statement</cap:event>
<cap:effective>2013-01-26T04:27:00-07:00</cap:effective>
<cap:expires>2013-01-26T15:00:00-07:00</cap:expires>
<cap:status>Actual</cap:status>
<cap:msgType>Alert</cap:msgType>
<cap:category>Met</cap:category>
<cap:urgency>Expected</cap:urgency>
<cap:severity>Minor</cap:severity>
<cap:certainty>Observed</cap:certainty>
<cap:areaDesc>Big and Little Wood River Region; Cache Valley, Idaho Portion; Caribou Highlands; Lost River, Pashimeroi; Sawtooth Mountains; South Central Highlands; Wasatch Mountains, Idaho Portion</cap:areaDesc>
<cap:polygon></cap:polygon>
<cap:geocode>
<valueName>FIPS6</valueName>
<value>016005 016007 016011 016013 016019 016023 016029 016031 016037 016041 016071 016077</value>
<valueName>UGC</valueName>
<value>IDZ018 IDZ022 IDZ023 IDZ024 IDZ025 IDZ031 IDZ032</value>
</cap:geocode>
<cap:parameter>
<valueName>VTEC</valueName>
<value></value>
</cap:parameter>
</entry>

<entry>
<id>http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE8F5A9F8.AirQualityAlert.124EE9142E78ID.MSOAQAMSO.738619c9bd434bd0bfbf7001349f0197</id>
<updated>2013-01-25T09:30:00-07:00</updated>
<published>2013-01-25T09:30:00-07:00</published>
<author>
<name>w-nws.webmaster@noaa.gov</name>
</author>
<title>Air Quality Alert issued January 25 at 9:30AM MST by NWS</title>
<link href="http://alerts.weather.gov/cap/wwacapget.php?x=ID124EE8F5A9F8.AirQualityAlert.124EE9142E78ID.MSOAQAMSO.738619c9bd434bd0bfbf7001349f0197"/>
<summary>...AN AIR QUALITY ADVISORY HAS BEEN ISSUED BY THE IDAHO DEPARTMENT OF ENVIRONMENTAL QUALITY... DUE TO SMOKE FROM WOOD BURNING FOR HOME HEATING...THE AIR QUALITY HAS BECOME UNHEALTHY FOR SENSITIVE GROUPS IN LEMHI COUNTY OF IDAHO INCLUDING THE CITIES OF SALMON. THIS ADVISORY WILL REMAIN IN EFFECT UNTIL AIR QUALITY HAS SIGNIFICANTLY IMPROVED.</summary>
<cap:event>Air Quality Alert</cap:event>
<cap:effective>2013-01-25T09:30:00-07:00</cap:effective>
<cap:expires>2013-01-27T09:30:00-07:00</cap:expires>
<cap:status>Actual</cap:status>
<cap:msgType>Alert</cap:msgType>
<cap:category>Met</cap:category>
<cap:urgency>Unknown</cap:urgency>
<cap:severity>Unknown</cap:severity>
<cap:certainty>Unknown</cap:certainty>
<cap:areaDesc>Lemhi</cap:areaDesc>
<cap:polygon></cap:polygon>
<cap:geocode>
<valueName>FIPS6</valueName>
<value>016059</value>
<valueName>UGC</valueName>
<value>IDC059</value>
</cap:geocode>
<cap:parameter>
<valueName>VTEC</valueName>
<value></value>
</cap:parameter>
</entry>
</feed>"""


# a sample empty cap feed
empty_cap = """<?xml version = '1.0' encoding = 'UTF-8' standalone = 'yes'?>


<id>http://alerts.weather.gov/cap/or.atom</id>
<logo>http://alerts.weather.gov/images/xml_logo.gif</logo>
<generator>NWS CAP Server</generator>
<updated>2013-01-26T20:58:01+00:00</updated>
<author>
<name>w-nws.webmaster@noaa.gov</name>
</author>
<title>Current Watches, Warnings and Advisories for Oregon Issued by the National Weather Service</title>
<link href='http://alerts.weather.gov/cap/or.atom'/>

<entry>
<id>http://alerts.weather.gov/cap/or.atom</id>
<updated>2013-01-26T20:58:01+00:00</updated>
<author>
<name>w-nws.webmaster@noaa.gov</name>
</author>
<title>There are no active watches, warnings or advisories</title>
<link href='http://alerts.weather.gov/cap/or.atom'/>
<summary>There are no active watches, warnings or advisories</summary>
</entry>
</feed>"""


class Test_Cap(unittest.TestCase):
    def setUp(self):
        pass

    def test_parser(self):
        c = CapParser(raw_cap=rc, geo=None)
        c.get_alerts()

    def test_empty_feed(self):
        c = CapParser(empty_cap)
        c.get_alerts()

if __name__ == '__main__':
    unittest.main()
