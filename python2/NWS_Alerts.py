#!/usr/bin/env python2

import sys
from weatheralerts import nws



if __name__ == u"__main__":
    if len(sys.argv) > 1:
        nwsalerts = nws.Alerts()
        req_type = sys.argv[1]
        if req_type == u'summary':
            result = nwsalerts.national_summary()
        if req_type == u'location':
            req_location = { u'county': sys.argv[2], u'state': sys.argv[3]}
            result = nwsalerts.activefor_county(req_location)
        if req_type == u'state':
            result = nwsalerts.state_summary(state=sys.argv[2])
        if req_type == u'samecodes':
            result = nwsalerts.activefor_samecodes(sys.argv[2])

        print result
    else:
        print u"No arguments supplied, please see the wiki"
