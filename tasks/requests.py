#!/usr/bin/env python

import datetime

import webapp2
from google.appengine.api import mail

from model.model import MeetingRequest


class RequestSummaryHandler(webapp2.RequestHandler):

    def get(self):

        one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
        old_pending_requests = MeetingRequest.query(
            MeetingRequest.state == 'pending' and
            MeetingRequest.created < one_month_ago
        ).order(MeetingRequest.created).fetch(100)

        users_notified = set()

        for request in old_pending_requests:

            parent_key = request.key.parent()
            if parent_key not in users_notified:

                users_notified.add(parent_key)

                user_email = parent_key.get().email
                self.send_notification_email_user(user_email)

    def send_notification_email_user(self, user_email):

        if mail.is_email_valid(user_email):

            sender_address = 'Lunch Mate <lunchmates@appid.appspotmail.com>'
            subject = 'Some of your lunchmates are still waiting for you'
            body = 'You have unaccepted invitations. Go check them out!'

            mail.send_mail(sender_address, user_email, subject, body)
