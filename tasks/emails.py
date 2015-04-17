#!/usr/bin/env python

import webapp2
from google.appengine.api import mail

from model.model import UserData

class EmailTaskHandler(webapp2.RequestHandler):

    def post(self):

        owner_id = self.request.get('owner_id')
        owner_email = UserData.get_by_id(int(owner_id)).email

        if mail.is_email_valid(owner_email):

            nickname = self.request.get('nickname')

            sender_address = 'Lunch Mate <lunchmates@appid.appspotmail.com>'
            subject = 'Request to join your meeting'
            body = '%s has requested to join your meeting!' % nickname

            mail.send_mail(sender_address, owner_email, subject, body)
