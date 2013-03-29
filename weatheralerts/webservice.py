import threading
from time import sleep
from datetime import datetime
import logging
from socket import gethostname
from weatheralerts import WeatherAlerts
import graypy
import paste
import json
try:
    from bottle import route, run, get, post, error, debug  #, response, request
except ImportError:
    logging.critical("Please install bottle")



class WebApp():
    def __init__(self):
        self._setup_logging()
        self.nws = WeatherAlerts(cachetime=5)
        self._alerts = self.nws._serialized_alerts
        self._threads = []
        self.shutdown = False

    @property
    def status(self):
        return {'alive': True,}

    def _setup_logging(self):
        if gethostname() == 'mc117':
            facilityname = "wxalertsws-dev"
            loglvl = logging.DEBUG
            logging.basicConfig(level=logging.DEBUG,
                                format='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
        else:
            facilityname = "wxalertsws"
            loglvl = logging.DEBUG


        handler = graypy.GELFHandler('logs', 12201)
        logging.root.name = facilityname
        logformat = logging.Formatter(fmt='%(asctime)s [%(levelname)s] (%(threadName)-10s) %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S')
        handler.setFormatter(logformat)
        logging.root.addHandler(handler)
        logging.root.setLevel(loglvl)
        logging.info("Logging Initialized")


    def start(self):
        logging.info("Initializing Threads")
        al = AlertsLoader(self)
        ws = WebService(self)

        self._threads.append(al)
        self._threads.append(ws)

        logging.info("Starting Threads")
        for thread in self._threads:
            thread.setDaemon(True)
            thread.start()

        while self.shutdown is False:
            self._main_loop()
        self.cleanup()

    def _main_loop(self):
        sleep(60)
        logging.debug("Heartbeat")


    def cleanup(self):
        logging.info("Cleaning up for shutdown")
        sys.exit()


class WebService(threading.Thread):
    def __init__(self, webapp):
        self.webapp = webapp
        threading.Thread.__init__(self)

    def run(self):
        self.setName("WEBSVC")
        logging.info("Starting WebService")
        while self.webapp.shutdown == False:
            sleep(1)
            self.server()


    def server(self):
        @route('/')
        def index():
            return ("NWS (CAP) WeatherAlerts JSON Webservice")

        #@error(500)
        #def errormsg():
            #return "ERROR 500: Sorry, something broke"

        #@error(404)
        #def notfound():
            #return "ERROR 404: These aren't the pages you're looking for"


        @route('/all')
        def all():
            return {'status': self.webapp.status,
                    'alerts': self.webapp._alerts}

        @route('/samecodes/:sc')
        def samecodes(sc):
            sc = sc.split(',')
            resuult = {'status': self.webapp.status,
                    'alerts': [x for x in self.webapp._alerts if list(set(x['samecodes']) & set(sc))]}
            return resuult



        run(host='0.0.0.0', port=8080, quiet=True, server='paste')









class AlertsLoader(threading.Thread):
    def __init__(self, webapp):
        self.webapp = webapp
        threading.Thread.__init__(self)

    def run(self):
        self.setName("AlertLoader")
        while self.webapp.shutdown == False:
            try:
                self.webapp.nws.refresh(force=True)
                self._alerts = self.webapp.nws._serialized_alerts
                self._sleeptillminute()
            except Exception as e:
                logging.critical(e, exc_info=1)

    def _sleeptillminute(self):
        t = datetime.utcnow()
        sleeptime = 60 - (t.second + t.microsecond/1000000.0)
        sleep(sleeptime)






if __name__ == "__main__":
    pass