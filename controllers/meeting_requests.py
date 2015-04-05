#!/usr/bin/env python

import base
from base import login_required

from util.format import *
from model.model import *

class MeetingRequestController(base.BaseHandler):
        
    @login_required
    def dispatch(self):        
        super(MeetingRequestController, self).dispatch()

    def get(self, meeting_id): # Returns the requests of a meeting

        results = []

        query = MeetingRequest.for_meeting(meeting_id)

        for request in query:
            results.append(request)

        self.respond(200, results)


    def post(self, meeting_id): # Posts a request to join a meeting

        # TODO Check if there's an invitation already
        request = MeetingRequest(parent=self.user_key, meeting=ndb.Key(Meeting, meeting_id))
        request.put()
        self.respond(201, request)
