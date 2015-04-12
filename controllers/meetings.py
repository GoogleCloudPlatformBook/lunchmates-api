#!/usr/bin/env python

import base
from base import login_required

from google.appengine.api import memcache

from util.format import *
from model.model import *

TOP_MEETINGS_KEY = "top_meetings"

class MeetingController(base.BaseHandler):
            
    @login_required
    def dispatch(self):        
        super(MeetingController, self).dispatch()

    def get(self):

        results = memcache.get(TOP_MEETINGS_KEY)

        if results is None:

            results = []
            query = Meeting.all().fetch(30)

            for meeting in query:
                results.append(meeting)

            memcache.set(TOP_MEETINGS_KEY, results, 30)

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
