#!/usr/bin/env python

import config

# Google's AppEngine modules
import webapp2
from webapp2 import Route
from webapp2_extras import routes
from webapp2_extras.routes import DomainRoute

# Controllers and handlers
from controllers.auth import *
from controllers.users import *
from controllers.meetings import *
from controllers.meeting_requests import *

# Task handlers
from tasks.emails import *

# Requested URLs that are not listed here return with a 404

FRONTEND_ROUTES = [
    DomainRoute(config.subdomain, [ # Allowed domains

    	routes.PathPrefixRoute(r'/api', [

    		# Sessions
            Route(r'/authenticate', handler=AuthHandler),

    		# Users
            Route(r'/users', handler=UserController),

	        # Meetings
            Route(r'/meetings', handler=MeetingController),
            routes.PathPrefixRoute(r'/meetings/<meeting_id:\d+>', [
                Route(r'/requests', handler=MeetingRequestController, methods=['GET']),
                Route(r'/join', handler=MeetingRequestController, methods=['POST'])
            ])  
	    ])
    ])
]
app = webapp2.WSGIApplication(FRONTEND_ROUTES, debug=True)


TASK_ROUTES = [
    DomainRoute(config.subdomain, [ # Allowed domains

        routes.PathPrefixRoute(r'/tasks', [

            # Emails
            Route(r'/email', handler=EmailTaskHandler)
        ])
    ])
]
tasks = webapp2.WSGIApplication(TASK_ROUTES, debug=True)