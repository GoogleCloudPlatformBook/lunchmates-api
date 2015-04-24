#!/usr/bin/env python

import json
import urllib
import base64

import webapp2
from google.appengine.api import mail

from model.model import MeetingRequest

from util.json_serializer import JsonSerializer

class MeetingsTaskHandler(webapp2.RequestHandler):
    ''' This class receives and processes messages from Pub/Sub'''

    def meetingFinished(self, meeting_id):

        # Email information
        sender_address = 'Lunch Mate <lunchmates@appid.appspotmail.com>'
        subject = 'How was your meeting'
        body = 'Rate your last meeting!'

        # Get the message from pub/sub
        message = json.loads(urllib.unquote(self.request.body).rstrip('='))
        message_data = base64.b64decode(str(message['message']['data']))

        finish_timestamp = int(message_data)

        # Get all accepted meeting requests
        query = MeetingRequest.for_meeting(int(meeting_id), 'accepted')
        for request in query:
            attendee = request.key.parent().get()

            if attendee is not None and mail.is_email_valid(attendee.email):
                mail.send_mail(sender_address, attendee.email, subject, body)
