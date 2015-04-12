#!/usr/bin/env python

import base
from base import login_required

from google.appengine.api import taskqueue

from util.format import *
from model.model import *

class MeetingRequestController(base.BaseHandler):
        
    @login_required
    def dispatch(self):        
        super(MeetingRequestController, self).dispatch()

    def get(self, meeting_id): # Returns the requests of a meeting

        results = []

        query = MeetingRequest.for_meeting(int(meeting_id))

        for request in query:
            results.append(request)

        self.respond(200, results)


    def post(self, meeting_id): # Posts a request to join a meeting

        # TODO Check if there's an invitation already
        meeting = Meeting.get_by_id(int(meeting_id))
        join_request = MeetingRequest(parent=self.user_key, meeting=meeting.key)
        join_request.put()

        # Schedule task to send email
        params = {'owner_id': meeting.owner.id(), 'nickname':self.user.nickname()}
        taskqueue.add(queue_name='email', url='/tasks/email', params=params)

        self.respond(201, join_request)
