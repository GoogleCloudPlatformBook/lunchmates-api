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
from tasks.meetings import *
from tasks.emails import *
from tasks.requests import *

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

            # Notifications (Pub/Sub)
            Route(r'/meetings/finished_event', handler='tasks.meetings.MeetingsTaskHandler:meetingFinished', methods=['POST']),

            # Emails
            Route(r'/email', handler=EmailTaskHandler),

            # Send users a request summary of their pending incoming requests
            Route(r'/request-summary', handler=RequestSummaryHandler)
        ])
    ])
]
tasks = webapp2.WSGIApplication(TASK_ROUTES, debug=True)