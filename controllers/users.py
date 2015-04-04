#!/usr/bin/env python

import base
from base import login_required

from model.model import *

class UserController(base.BaseHandler):

    @login_required       
    def get(self):

        results = []

        # Retrieve attendees
        q = UserData.all()

        for user in q:
            results.append(user)

        self.respond(200, results)