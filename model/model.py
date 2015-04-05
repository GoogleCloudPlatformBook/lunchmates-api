#!/usr/bin/env python

import unicodedata

from google.appengine.ext import ndb
from google.appengine.api import users

PROVIDER_GOOGLE = 'google'
PROVIDER_FACEBOOK = 'facebook'

DATE_FORMAT_STR = '%Y-%m-%dT%H:%M'

class BaseModel(ndb.Model):
    created = ndb.DateTimeProperty(auto_now_add=True)

    @classmethod
    def all(cls):
        return cls.query().order(-cls.created)

    def to_dict(self, exclude=None):
        dict = super(BaseModel, self).to_dict(exclude=exclude)
        dict['id'] = self.key.id()
        return dict

    def __hash__(self):
        return self.key.id()

    def __eq__(self, other):
        return self.key.id() == other.key.id()
      

class UserData(BaseModel):
    auth_provider = ndb.StringProperty(choices=[PROVIDER_GOOGLE, PROVIDER_FACEBOOK], required=True)
    username = ndb.StringProperty(default='')
    search_username = ndb.ComputedProperty(lambda self: unicodedata.normalize('NFKD', unicode(self.username)).encode('ascii','ignore').lower())
    email = ndb.StringProperty(required=True)

    @classmethod
    def create_user(cls, external_user, provider, user_key):

        user = UserData(auth_provider=provider)
        user.key = user_key
        
        if provider == PROVIDER_GOOGLE:
            user.email = external_user.email()
            user.username = external_user.nickname()

        elif provider == PROVIDER_FACEBOOK:
            pass

        else:
            raise ValueError('Provider is unknown: ' + provider)

        user.put()
        return user


class Meeting(BaseModel):
    venue_forsquare_id = ndb.StringProperty(required=True)
    location = ndb.GeoPtProperty()
    earliest_possible_start = ndb.DateTimeProperty(required=True)
    latest_possible_start = ndb.DateTimeProperty()
    topic = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True, choices=['drink', 'lunch', 'brunch'])
    tags = ndb.StringProperty(repeated=True)


class MeetingRequest(BaseModel):
    meeting = ndb.KeyProperty(kind=Meeting, required=True)
    state = ndb.StringProperty(default='pending', choices=['pending', 'accepted', 'rejected'])

    @classmethod
    def for_meeting(cls, meeting_id):
        return cls.query(cls.meeting==ndb.Key(Meeting, meeting_id)).order(-cls.created)

    def to_dict(self):
        return super(MeetingRequest, self).to_dict(exclude=['meeting'])


