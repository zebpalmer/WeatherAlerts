The code is VERY raw, but what is here, does work. I'll be refining and standardizing as it is
incorperated into a personal project. This code is provided under GPLv3 (see LICENSE.txt).
If you do make improvements for your own use, please contribute back to this project.
You can submit a git pull request or even email me: zeb@zebpalmer.com

You can find this project's home at http://git.zebpalmer.com/nws-alerts
and me on Google Plus http://zebpalmer.com/+

If you'd like to contribute or want to know what is planned, check out TODO.txt.
I certainly welcome new features, improvments and of course bug fixes.



NOTES:
Currently the performance parsing the entire US alert feed isn't great (about a second on decent hardware, 3-4 seconds
on slower hardware) but in most use cases this won't be needed. When running for a state summary or specific location, 
we grab and parse the state feed, which is much smaller.

There are three use cases that I am moving to support first. 1) command line usage (or calling from
another script) 2) Usage via a Nagios (or similar) monitoring script 3) powering a web api that given
various paramaters will return json objects or raw text summaries of the requested data.
