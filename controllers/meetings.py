#!/usr/bin/env python

import base
from base import login_required

from util.format import *
from model.model import *

class MeetingController(base.BaseHandler):
            
    @login_required
    def dispatch(self):        
        super(MeetingController, self).dispatch()

    def get(self):

        results = []

        query = Meeting.all()

        for meeting in query:
            results.append(meeting)

        self.respond(200, results)


    @ndb.transactional(xg=True)
    def post(self):

        if self.inputBody:

            # Pre-format
            self.inputBody['earliest_possible_start'] = format_to_date(self.inputBody['earliest_possible_start'], DATE_FORMAT_STR)
            self.inputBody['latest_possible_start'] = format_to_date(self.inputBody['latest_possible_start'], DATE_FORMAT_STR)
            self.inputBody['location'] = format_to_geo_pos(self.inputBody['location'])

            # Put meeting
            meeting = Meeting(parent=self.user_key, **self.inputBody)
            meeting.put()

            # Increment meeting counter for user
            MeetingCounter.increment(self.user_key)

            self.respond(201, meeting)

        else:
            self.respond(422, {base.ERRORS: "Request must have a body"})
