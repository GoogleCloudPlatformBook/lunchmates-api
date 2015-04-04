#!/usr/bin/env python

# Google's AppEngine modules:
import webapp2
from webapp2 import Route
from webapp2_extras import routes
from webapp2_extras.routes import DomainRoute

# Controllers and handlers
from controllers.sessions import *
from controllers.users import *
from controllers.meetings import *

# Requested URLs that are not listed here,
# will return 404

ROUTES = [
    DomainRoute('<:(lunch--mates\.appspot\.com|localhost)>', [ # Allowed domains

    	routes.PathPrefixRoute(r'/api', [

    		# Sessions
    		Route(r'/signup', handler=SignupHandler),

    		# Users
	        Route(r'/users', handler=UserController),

	        # Meetings
	        Route(r'/meetings', handler=MeetingController),
	        
	    ])
    ])
]

app = webapp2.WSGIApplication(ROUTES, debug=True)