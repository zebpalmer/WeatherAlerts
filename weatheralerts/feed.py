import os
import re
import requests
from xml.dom import minidom
from datetime import datetime, timedelta
import tempfile

from geo import GeoDB


class AlertsFeed(object):
    '''Fetch the NWS CAP/XML Alerts feed for the US or a single state if requested
       if an instance of the GeoDB class has already been created, you can pass that
       as well to save some processing'''
    def __init__(self, state='US', maxage=3, feedreload=False):
        self._alerts = ''
        self._feedstatus = ''
        self._cachetime = maxage
        self._state = state
        self._cachedir = str(tempfile.gettempdir()) + '/'
        self._feed_cache_file = self._cachedir + 'nws_alerts_%s.cache' % (self._state)
        self._cachetime = 3
        self._lookuptable = {}
        self._get_alerts_feed()

    def _get_feed_cache(self):
        '''If a recent cache exists, return it, else return None'''
        feed_cache = None
        if os.path.exists(self._feed_cache_file):
            maxage = datetime.now() - timedelta(minutes=self._cachetime)
            file_ts = datetime.fromtimestamp(os.stat(self._feed_cache_file).st_mtime)
            if file_ts > maxage:
                try:
                    with open(self._feed_cache_file, 'rb') as cache:
                        feed_cache = cache.read()
                except Exception:
                    pass
        return feed_cache

    def _get_alerts_feed(self, refresh=False):
        '''Load the alerts feed and parse it'''
        cached = self._get_feed_cache()
        if refresh is True or cached is None:
            self._raw_feed = self._get_nws_feed()
            self._save_feed_cache(self._raw_feed)
        else:
            self._raw_feed = cached
        return self._raw_feed

    def _get_nws_feed(self):
        '''get nws alert feed, and cache it'''
        url = '''http://alerts.weather.gov/cap/%s.php?x=0''' % (self._state)
        xml = requests.get(url).content
        return xml

    def _save_feed_cache(self, raw_feed):
        with open(self._feed_cache_file, 'wb') as cache:
            cache.write(raw_feed)

if __name__ == '__main__':
    feed = AlertsFeed(state='ID')
