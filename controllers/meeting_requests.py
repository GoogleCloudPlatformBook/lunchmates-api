#!/usr/bin/env python

import base
from base import login_required

from google.appengine.api import mail

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

        owner_email = meeting.owner.get().email
        if mail.is_email_valid(owner_email):
            self._send_join_request_notification(owner_email, self.user.nickname())

        self.respond(201, join_request)



    def _send_join_request_notification(self, email_address, nickname):

        sender_address = 'Lunch Mate <lunchmates@appid.appspotmail.com>'
        subject = 'Request to join your meeting'
        body = '%s has requested to join your meeting!' % nickname

        mail.send_mail(sender_address, email_address, subject, body)
