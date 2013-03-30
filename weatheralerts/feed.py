import sys
import os
import requests
from datetime import datetime, timedelta
import tempfile


class AlertsFeed(object):
    '''Fetch the NWS CAP/XML Alerts feed for the US or a single state if requested
       if an instance of the GeoDB class has already been created, you can pass that
       as well to save some processing
       This will cache the feed (in local tempdir) for up to 'maxage' minutes'''
    def __init__(self, state='US', maxage=3):
        self._alerts = ''
        self._feedstatus = ''
        self._cachetime = maxage
        self._state = state
        self._cachedir = str(tempfile.gettempdir()) + '/'
        self._feed_cache_file = self._cachedir + 'nws_alerts_py{0}_{1}.cache'.format(sys.version_info[0], self._state)
        self._cachetime = 3

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
                finally:
                    pass
        return feed_cache

    def raw_cap(self, refresh=False):
        '''
        Raw xml(cap) of the the feed. If a valid cache is availible
        it is used, else a new copy of the feed is grabbed
        Note: you can force refresh here, if you do, don't also manually call refresh
        '''
        raw = self._get_feed_cache()
        if raw is None or refresh is True:
            raw = self.refresh()
        return raw

    def refresh(self):
        '''
        NOTE: You probably don't want to call this... This does not update the alerts loaded
        in the WeatherAlerts object, only the underlying feed. This is only used internally now and as such,
        will likely be deprecated soon. Please call `WeatherAlerts.refresh()` instead.
        '''
        raw = self._get_nws_feed()
        self._save_feed_cache(raw)
        return raw


    def _get_nws_feed(self):
        '''get nws alert feed, and cache it'''
        url = '''http://alerts.weather.gov/cap/%s.php?x=0''' % (str(self._state).lower())
        # pylint: disable=E1103
        xml = requests.get(url).content
        return xml

    def _save_feed_cache(self, raw_feed):
        with open(self._feed_cache_file, 'wb') as cache:
            cache.write(raw_feed)
