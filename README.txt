The code is pretty raw, but what is here, does work. I'll be refining it as it is
incorperated into a personal project. This code is provided under GPLv3 (see LICENSE.txt).
If you do make improvements, please contribute back to this project.
You can submit a git pull request or email me: zeb@zebpalmer.com

You can find this project's home at http://git.zebpalmer.com/nws-alerts
and me on Google Plus http://zebpalmer.com/+

If you'd like to contribute or want to know what is planned, check out TODO.txt.
I certainly welcome new features, improvments and of course bug fixes.


USAGE:
--Command Line--
To check for alerts at a given location, run.   'python nws_alerts.py location County ST'
that is the run type "location" followed by your county (first leter capitalized) and two letter 
state abbreviation (capitalized).   

You can also run a state summary 'python nws_alerts.py state ST' with 'ST' being the two letter 
abbreviation. This will display all active alerts in the state, with the affected locations.   


PERFORMANCE:
Currently the performance parsing the entire US alert feed (on an active weather day) isn't great (about a second on decent hardware, 3-4 seconds
on slow hardware) but in most use cases this won't be needed. When running for a state summary or specific location, 
we grab and parse the state feed, which is much smaller.


FUTURE:
There are three use cases that I am moving to support first. 1) command line usage (or calling from
another script) 2) Usage via a Nagios (or similar) monitoring script 3) powering a web api that given
various paramaters will return json or raw text summaries of the requested data. If you have 
another use case, feel free to submit a request and jump in to help if you can. 
