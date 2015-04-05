#!/usr/bin/env python

import webapp2
import json
import re

from model.model import UserData

from google.appengine.ext import ndb
from google.appengine.api import users

from util.json_serializer import JsonSerializer

ACCESS_CONTROL_ALLOW_ORIGIN = 'Access-Control-Allow-Origin'
CONTENT_TYPE_HEADER = 'Content-Type'
ORIGIN_HEADER = 'Origin'
JSON_CONTENT_TYPE = 'application/json'

API_ERROR = 'api_error'
VALIDATION_ERROR = 'validation_error'

INVALID_FIELD = VALIDATION_ERROR + '.invalid_field'
MANDATORY_FIELD = VALIDATION_ERROR + '.mandatory_field'
FIELD_TOO_LONG = VALIDATION_ERROR + '.field_too_long'

NOT_AUTHORIZED = 'Not authorized'

ERRORS = 'errors'
MESSAGE = 'message'

AUTHORIZATION = 'Authorization'

def login_required(handler):
    '''Requires that a user be logged in to access the resource'''

    def check_login(self, *args, **kwargs):     
        if not self.user:
            return self.redirect(users.create_login_url(self.request.path))
        else:
            return handler(self, *args, **kwargs)

    return check_login 

class BaseHandler(webapp2.RequestHandler):

    def __init__(self, request=None, response=None, requires_authentication=False):
        super(BaseHandler, self).__init__(request, response)

        self.setupResponse()

        self.inputBody = dict()
        if self.request.body:
            self.inputBody = json.loads(self.request.body)

    @webapp2.cached_property
    def user(self):
        user = users.get_current_user()
        return user

    @webapp2.cached_property
    def user_key(self):
        return ndb.Key(UserData, self.user.user_id())

    def setupResponse(self):
        self.request.path_info_pop()
        self.headers = self.request.headers

        self.response.status = 404        
        self.response.headers[CONTENT_TYPE_HEADER] = JSON_CONTENT_TYPE

    def respond(self, status_code, body = None):
        self.response.status = status_code
        self.response.write(json.dumps(body, cls = JsonSerializer, indent=4) if body is not None else '{}')