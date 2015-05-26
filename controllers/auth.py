#!/usr/bin/env python

import base
from base import login_required

from model import model
from model.model import *

EMAIL_FIELD = 'email'
EMAIL_REGEX = ('[a-zA-Z0-9\\+\\.\\_\\%\\-\\+]{1,256}\\@[a-zA-Z0-9]'
               '[a-zA-Z0-9\\-]{0,64}(\\.[a-zA-Z0-9][a-zA-Z0-9\\-]{0,25})')

USER_EXISTS = base.VALIDATION_ERROR + '.user_already_exists'
INCORRECT_CREDENTIALS = base.VALIDATION_ERROR + '.invalid_credentials'

PASSWORD_FIELD = 'password'
NAME_FIELD = 'name'


class AuthHandler(base.BaseHandler):

    @login_required
    def post(self):

        key = self.user_key
        user = key.get()

        if user is None:

            # User does not exist, go ahead and create
            user = UserData.create_user(self.user, model.PROVIDER_GOOGLE, key)

        self.respond(201, user)
